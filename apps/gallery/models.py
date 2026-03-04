from django.db import models
from apps.services.models import Service

class GalleryItem(models.Model):
    title = models.CharField(max_length=200)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    before_image = models.ImageField(upload_to='gallery/before/', blank=True, null=True)
    after_image = models.ImageField(upload_to='gallery/after/')
    description = models.TextField(blank=True)
    vehicle_type = models.CharField(max_length=100, blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title
