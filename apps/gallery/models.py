from django.db import models
from apps.services.models import Service

class GalleryItem(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    title        = models.CharField(max_length=200)
    service      = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    media_type   = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')

    # Images
    before_image = models.ImageField(upload_to='gallery/before/', blank=True, null=True)
    after_image  = models.ImageField(upload_to='gallery/after/', blank=True, null=True)

    # Video
    video        = models.FileField(upload_to='gallery/videos/', blank=True, null=True)
    video_thumbnail = models.ImageField(upload_to='gallery/thumbnails/', blank=True, null=True)

    description  = models.TextField(blank=True)
    vehicle_type = models.CharField(max_length=100, blank=True)
    is_featured  = models.BooleanField(default=False)
    order        = models.PositiveIntegerField(default=0)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    @property
    def is_video(self):
        return self.media_type == 'video'

    @property
    def thumbnail(self):
        if self.video_thumbnail:
            return self.video_thumbnail
        if self.after_image:
            return self.after_image
        return None
