from django.shortcuts import render
from .models import GalleryItem
from apps.services.models import Service

def gallery(request):
    service_filter = request.GET.get('service', '')
    type_filter = request.GET.get('type', '')
    items = GalleryItem.objects.select_related('service').all()
    if service_filter:
        items = items.filter(service__slug=service_filter)
    if type_filter in ('image', 'video'):
        items = items.filter(media_type=type_filter)
    services = Service.objects.filter(is_active=True)
    return render(request, 'gallery/gallery.html', {
        'items': items,
        'services': services,
        'service_filter': service_filter,
        'type_filter': type_filter,
    })
