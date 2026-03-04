from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from apps.bookings.models import Booking
from apps.bookings.forms import BookingStatusForm
from apps.gallery.models import GalleryItem
from apps.gallery.forms import GalleryItemForm
from apps.services.models import Service, ServicePricing
from apps.services.forms import ServiceForm, ServicePricingFormSet
from apps.inquiries.models import Inquiry


def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user and user.is_staff:
            login(request, user)
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


@login_required
def gallery_add(request):
    form = GalleryItemForm()
    if request.method == 'POST':
        form = GalleryItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gallery item added.')
            return redirect('admin_gallery')
    return render(request, 'admin_panel/gallery/form.html', {'form': form, 'title': 'Add Gallery Item'})


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
    return render(request, 'admin_panel/gallery/form.html', {'form': form, 'title': 'Edit Gallery Item'})


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


@login_required
def service_add(request):
    form = ServiceForm()
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service added.')
            return redirect('admin_services')
    return render(request, 'admin_panel/services/form.html', {'form': form, 'title': 'Add Service'})


@login_required
def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    form = ServiceForm(instance=service)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated.')
            return redirect('admin_services')
    return render(request, 'admin_panel/services/form.html', {'form': form, 'title': 'Edit Service'})


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
