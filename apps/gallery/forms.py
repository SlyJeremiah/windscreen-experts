from django import forms
from django.core.files.storage import default_storage

from .models import GalleryItem

# Files posted through the Vercel function are limited to 4.5 MB per request.
# Larger files (phone photos/videos) are uploaded straight to storage by the
# browser and only their storage key is posted - see admin_views.gallery_upload_url.
MAX_UPLOAD_MB = 4
MAX_DIRECT_UPLOAD_MB = 200

FILE_FIELDS = ('before_image', 'after_image', 'video', 'video_thumbnail')
UPLOAD_FOLDERS = {
    'before_image': 'gallery/before/',
    'after_image': 'gallery/after/',
    'video': 'gallery/videos/',
    'video_thumbnail': 'gallery/thumbnails/',
}


class GalleryItemForm(forms.ModelForm):
    # Storage keys of files the browser already uploaded directly to storage
    before_image_key    = forms.CharField(required=False, widget=forms.HiddenInput)
    after_image_key     = forms.CharField(required=False, widget=forms.HiddenInput)
    video_key           = forms.CharField(required=False, widget=forms.HiddenInput)
    video_thumbnail_key = forms.CharField(required=False, widget=forms.HiddenInput)

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
            'order':        forms.NumberInput(attrs={'class': 'form-control', 'inputmode': 'numeric'}),
            'before_image':    forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'after_image':     forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'video':           forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'video/*'}),
            'video_thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def _clean_key(self, field):
        key = (self.cleaned_data.get(f'{field}_key') or '').strip()
        if not key:
            return ''
        # Only accept keys in this field's own folder that really exist in storage
        if not key.startswith(UPLOAD_FOLDERS[field]) or '..' in key or not default_storage.exists(key):
            self.add_error(field, 'The uploaded file could not be found. Please try uploading it again.')
            return ''
        return key

    def clean(self):
        cleaned_data = super().clean()
        media_type   = cleaned_data.get('media_type')

        self.direct_keys = {}
        for field in FILE_FIELDS:
            key = self._clean_key(field)
            if key:
                self.direct_keys[field] = key

        def has_file(field):
            return bool(cleaned_data.get(field) or field in self.direct_keys or
                        (self.instance.pk and getattr(self.instance, field)))

        if media_type == 'image' and not has_file('after_image'):
            self.add_error('after_image', 'Please upload an after image.')

        if media_type == 'video' and not has_file('video'):
            self.add_error('video', 'Please upload a video file.')

        for field in FILE_FIELDS:
            f = cleaned_data.get(field)
            if f and getattr(f, 'size', 0) > MAX_UPLOAD_MB * 1024 * 1024:
                self.add_error(field, f'File is too large ({f.size / 1024 / 1024:.1f} MB). '
                                      f'Please keep uploads under {MAX_UPLOAD_MB} MB.')

        return cleaned_data

    def save(self, commit=True):
        item = super().save(commit=False)
        for field, key in getattr(self, 'direct_keys', {}).items():
            getattr(item, field).name = key
        if commit:
            item.save()
            self.save_m2m()
        return item
