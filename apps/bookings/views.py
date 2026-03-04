from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import BookingForm
from .models import Booking

def booking_create(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            # Email confirmation to customer
            try:
                send_mail(
                    subject=f'Booking Confirmed – Windscreen Experts #{booking.pk}',
                    message=f"""Hi {booking.full_name},

Your booking has been received! Here are your details:

Service: {booking.service}
Date: {booking.preferred_date}
Time: {booking.preferred_time}
Location: {booking.location}
Vehicle: {booking.vehicle_type} {booking.vehicle_make} {booking.vehicle_model}

We will confirm your booking shortly. First-time customers receive 20% off!

Contact us: +263 77 786 7884 | munashe@windowscreens.co.zw

– Windscreen Experts Team
""",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[booking.email],
                    fail_silently=True,
                )
                # Notify admin
                send_mail(
                    subject=f'New Booking #{booking.pk} – {booking.full_name}',
                    message=f'New booking from {booking.full_name} ({booking.email}, {booking.phone})\nService: {booking.service}\nDate: {booking.preferred_date} at {booking.preferred_time}\nLocation: {booking.location}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(request, f'Booking submitted! We\'ll contact you at {booking.phone} to confirm.')
            return redirect('booking_success')
    return render(request, 'bookings/create.html', {'form': form})


def booking_success(request):
    return render(request, 'bookings/success.html')
