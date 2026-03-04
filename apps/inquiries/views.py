from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import InquiryForm

def inquiry_create(request):
    form = InquiryForm()
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            try:
                send_mail(
                    subject=f'New Inquiry – {inquiry.subject}',
                    message=f'From: {inquiry.name} ({inquiry.email}, {inquiry.phone})\n\n{inquiry.message}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(request, 'Your inquiry has been sent! We\'ll be in touch soon.')
            return redirect('inquiry_success')
    return render(request, 'inquiries/form.html', {'form': form})

def inquiry_success(request):
    return render(request, 'inquiries/success.html')
