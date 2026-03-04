from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    icon = models.CharField(max_length=100, help_text='Bootstrap icon class e.g. bi-tools', blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class ServicePricing(models.Model):
    VEHICLE_CHOICES = [
        ('compact', 'Compact'),
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('van', 'Van'),
        ('other', 'Other'),
    ]
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='pricing')
    vehicle_type = models.CharField(max_length=50, choices=VEHICLE_CHOICES, blank=True)
    label = models.CharField(max_length=100, help_text='e.g. "Chip Repair" or leave blank for vehicle type pricing')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_starting_price = models.BooleanField(default=True, help_text='Show as "from $X"')

    class Meta:
        ordering = ['price']

    def __str__(self):
        return f"{self.service.name} – {self.label or self.vehicle_type} ${self.price}"
