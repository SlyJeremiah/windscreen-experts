from django import forms
from .models import GalleryItem

class GalleryItemForm(forms.ModelForm):
    class Meta:
        model  = GalleryItem
        fields = [
            'title', 'service', 'media_type',
            'before_image', 'after_image',
            'video', 'video_thumbnail',
            'description', 'vehicle_type', 'is_featured', 'order',
        ]
        widgets = {
            'title':        forms.TextInput(attrs={'class': 'form-control'}),
            'service':      forms.Select(attrs={'class': 'form-select'}),
            'media_type':   forms.Select(attrs={'class': 'form-select', 'id': 'id_media_type'}),
            'description':  forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'vehicle_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Sedan'}),
            'order':        forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        media_type   = cleaned_data.get('media_type')
        after_image  = cleaned_data.get('after_image')
        video        = cleaned_data.get('video')

        if media_type == 'image' and not after_image:
            # Only require after_image for image type if not already saved
            if not self.instance.pk or not self.instance.after_image:
                self.add_error('after_image', 'Please upload an after image.')

        if media_type == 'video' and not video:
            if not self.instance.pk or not self.instance.video:
                self.add_error('video', 'Please upload a video file.')

        return cleaned_data