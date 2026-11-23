import json
import os
import uuid

from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import get_valid_filename
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from apps.bookings.models import Booking
from apps.bookings.forms import BookingStatusForm
from apps.gallery.models import GalleryItem
from apps.gallery.forms import GalleryItemForm, MAX_DIRECT_UPLOAD_MB, UPLOAD_FOLDERS
from apps.services.models import Service, ServicePricing
from apps.services.forms import ServiceForm, ServicePricingFormSet
from apps.inquiries.models import Inquiry


# Only staff accounts may use the admin panel (plain logged-in users are sent to login)
login_required = user_passes_test(lambda u: u.is_active and u.is_staff, login_url='admin_login')


def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username', ''),
            password=request.POST.get('password', ''),
        )
        if user and user.is_staff:
            login(request, user)
            next_url = request.GET.get('next', '')
            if next_url.startswith('/admin-panel/'):
                return redirect(next_url)
            return redirect('admin_dashboard')
        messages.error(request, 'Invalid credentials or insufficient permissions.')
    return render(request, 'admin_panel/login.html')


def admin_logout(request):
    logout(request)
    return redirect('admin_login')


@login_required
def dashboard(request):
    context = {
        'total_bookings': Booking.objects.count(),
        'pending_bookings': Booking.objects.filter(status='pending').count(),
        'confirmed_bookings': Booking.objects.filter(status='confirmed').count(),
        'completed_bookings': Booking.objects.filter(status='completed').count(),
        'new_inquiries': Inquiry.objects.filter(status='new').count(),
        'recent_bookings': Booking.objects.select_related('service').order_by('-created_at')[:5],
        'recent_inquiries': Inquiry.objects.order_by('-created_at')[:5],
    }
    return render(request, 'admin_panel/dashboard.html', context)


# ── BOOKINGS ──
@login_required
def booking_list(request):
    qs = Booking.objects.select_related('service').all()
    status_filter = request.GET.get('status', '')
    search = request.GET.get('q', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    if search:
        qs = qs.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search))
    return render(request, 'admin_panel/bookings/list.html', {
        'bookings': qs,
        'status_filter': status_filter,
        'search': search,
        'status_choices': Booking.STATUS_CHOICES,
    })


@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    form = BookingStatusForm(instance=booking)
    if request.method == 'POST':
        form = BookingStatusForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking updated.')
            return redirect('admin_booking_detail', pk=pk)
    return render(request, 'admin_panel/bookings/detail.html', {'booking': booking, 'form': form})


@login_required
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking deleted.')
        return redirect('admin_bookings')
    return render(request, 'admin_panel/confirm_delete.html', {'object': booking, 'back_url': 'admin_bookings'})


# ── GALLERY ──
@login_required
def gallery_list(request):
    items = GalleryItem.objects.select_related('service').all()
    return render(request, 'admin_panel/gallery/list.html', {'items': items})


def direct_uploads_enabled():
    """True when media lives in S3-compatible storage (Backblaze B2) that browsers can PUT to."""
    return hasattr(default_storage, 'bucket_name') and hasattr(default_storage, 'connection')


@login_required
@require_POST
def gallery_upload_url(request):
    """Give the browser a short-lived link to upload one gallery file straight to storage.

    Phone photos and videos are usually bigger than the 4.5 MB a Vercel function
    accepts, so the browser sends the file to B2 itself and posts only the storage key.
    """
    if not direct_uploads_enabled():
        return JsonResponse({'error': 'Direct uploads are not available.'}, status=400)
    try:
        data = json.loads(request.body)
    except ValueError:
        return JsonResponse({'error': 'Invalid request.'}, status=400)

    field = data.get('field')
    content_type = str(data.get('content_type') or '')
    size = data.get('size')
    if field not in UPLOAD_FOLDERS:
        return JsonResponse({'error': 'Unknown field.'}, status=400)
    if not content_type.startswith('video/' if field == 'video' else 'image/'):
        kind = 'a video' if field == 'video' else 'an image'
        return JsonResponse({'error': f'Please choose {kind} file.'}, status=400)
    if not isinstance(size, int) or size <= 0 or size > MAX_DIRECT_UPLOAD_MB * 1024 * 1024:
        return JsonResponse({'error': f'Files must be under {MAX_DIRECT_UPLOAD_MB} MB.'}, status=400)

    filename = get_valid_filename(os.path.basename(str(data.get('filename') or 'upload')))
    name, ext = os.path.splitext(filename)
    key = f"{UPLOAD_FOLDERS[field]}{uuid.uuid4().hex[:12]}-{(name or 'upload')[:60]}{ext[:10].lower()}"
    client = default_storage.connection.meta.client
    url = client.generate_presigned_url(
        'put_object',
        Params={'Bucket': default_storage.bucket_name, 'Key': key, 'ContentType': content_type},
        ExpiresIn=900,
    )
    return JsonResponse({'url': url, 'key': key})


def _gallery_form_page(request, form, title):
    return render(request, 'admin_panel/gallery/form.html', {
        'form': form, 'title': title, 'direct_uploads': direct_uploads_enabled(),
    })


@login_required
def gallery_add(request):
    form = GalleryItemForm()
    if request.method == 'POST':
        form = GalleryItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gallery item added.')
            return redirect('admin_gallery')
    return _gallery_form_page(request, form, 'Add Gallery Item')


@login_required
def gallery_edit(request, pk):
    item = get_object_or_404(GalleryItem, pk=pk)
    form = GalleryItemForm(instance=item)
    if request.method == 'POST':
        form = GalleryItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gallery item updated.')
            return redirect('admin_gallery')
    return _gallery_form_page(request, form, 'Edit Gallery Item')


@login_required
def gallery_delete(request, pk):
    item = get_object_or_404(GalleryItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Gallery item deleted.')
        return redirect('admin_gallery')
    return render(request, 'admin_panel/confirm_delete.html', {'object': item, 'back_url': 'admin_gallery'})


# ── SERVICES ──
@login_required
def service_list(request):
    services = Service.objects.prefetch_related('pricing').all()
    return render(request, 'admin_panel/services/list.html', {'services': services})


def _service_form(request, service, title, success_msg):
    form = ServiceForm(request.POST or None, instance=service)
    formset = ServicePricingFormSet(request.POST or None, instance=service or Service(), prefix='pricing')
    if request.method == 'POST' and form.is_valid() and formset.is_valid():
        service = form.save()
        formset.instance = service
        formset.save()
        messages.success(request, success_msg)
        return redirect('admin_services')
    return render(request, 'admin_panel/services/form.html', {
        'form': form, 'formset': formset, 'title': title,
    })


@login_required
def service_add(request):
    return _service_form(request, None, 'Add Service', 'Service added.')


@login_required
def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return _service_form(request, service, 'Edit Service', 'Service updated.')


@login_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted.')
        return redirect('admin_services')
    return render(request, 'admin_panel/confirm_delete.html', {'object': service, 'back_url': 'admin_services'})


# ── INQUIRIES ──
@login_required
def inquiry_list(request):
    inquiries = Inquiry.objects.all()
    return render(request, 'admin_panel/inquiries/list.html', {'inquiries': inquiries})


@login_required
def inquiry_detail(request, pk):
    inquiry = get_object_or_404(Inquiry, pk=pk)
    if inquiry.status == 'new':
        inquiry.status = 'read'
        inquiry.save()
    return render(request, 'admin_panel/inquiries/detail.html', {'inquiry': inquiry})


# ── CUSTOMERS ──
@login_required
def customer_list(request):
    customers = (
        Booking.objects
        .values('email', 'first_name', 'last_name', 'phone')
        .annotate(booking_count=Count('id'))
        .order_by('-booking_count')
    )
    return render(request, 'admin_panel/customers/list.html', {'customers': customers})
