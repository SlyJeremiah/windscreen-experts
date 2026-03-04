from django.db import models
from apps.services.models import Service

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    VEHICLE_CHOICES = [
        ('compact', 'Compact'),
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('van', 'Van'),
        ('other', 'Other'),
    ]

    # Customer info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    # Booking details
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    vehicle_type = models.CharField(max_length=50, choices=VEHICLE_CHOICES)
    vehicle_make = models.CharField(max_length=100, blank=True)
    vehicle_model = models.CharField(max_length=100, blank=True)
    vehicle_year = models.PositiveIntegerField(null=True, blank=True)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    location = models.CharField(max_length=300, help_text='Address for mobile service')
    notes = models.TextField(blank=True)

    # Admin fields
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"#{self.pk} – {self.first_name} {self.last_name} ({self.service})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
