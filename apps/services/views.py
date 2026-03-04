from django.shortcuts import render
from .models import Service

def service_list(request):
    services = Service.objects.filter(is_active=True).prefetch_related('pricing')
    return render(request, 'services/list.html', {'services': services})

def service_detail(request, slug):
    from django.shortcuts import get_object_or_404
    service = get_object_or_404(Service, slug=slug, is_active=True)
    return render(request, 'services/detail.html', {'service': service})
