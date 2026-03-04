from django.shortcuts import render
from apps.services.models import Service
from apps.gallery.models import GalleryItem

WHY_ITEMS = [
    ('bi-lightning-charge', 'Fast Turnaround', 'Most repairs completed in under an hour. We respect your time.'),
    ('bi-geo-alt', 'Mobile Service', 'We come to your home, office, or wherever is convenient in Harare.'),
    ('bi-shield-check', 'Quality Guaranteed', 'Premium materials and expert technicians ensuring lasting results.'),
    ('bi-tag', 'Best Prices', 'Competitive rates with 20% off for first-time customers. Always transparent.'),
    ('bi-sun', 'UV & Heat Protection', 'Our films block UV rays and reduce cabin heat — protecting you and your car.'),
    ('bi-clock', 'Always Open', "We're available whenever you need us — 24/7."),
]

CONTACT_ITEMS = [
    ('bi-telephone', 'Phone', '+263 77 786 7884', 'tel:+263777867884'),
    ('bi-whatsapp', 'WhatsApp', '+263 71 988 8441', 'https://wa.me/263719888441'),
    ('bi-envelope', 'Email', 'munashe@windowscreens.co.zw', 'mailto:munashe@windowscreens.co.zw'),
    ('bi-geo-alt', 'Location', 'Mount Pleasant Shops, Harare', None),
    ('bi-clock', 'Hours', 'Always Open – 24/7', None),
    ('bi-globe', 'Website', 'windowsexp.co.zw', 'https://windowsexp.co.zw'),
]

ABOUT_STATS = [
    ('bi-car-front', 'Cars Serviced', '500+'),
    ('bi-clock', 'Always Available', '24/7'),
    ('bi-percent', 'First Visit Off', '20%'),
    ('bi-tools', 'Core Services', '4'),
]

def home(request):
    services = Service.objects.filter(is_active=True).prefetch_related('pricing')[:4]
    featured = GalleryItem.objects.filter(is_featured=True)[:6]
    return render(request, 'core/home.html', {'services': services, 'featured': featured, 'why_items': WHY_ITEMS})

def about(request):
    stats = [('Cars Serviced','500+'),('Always Available','24/7'),('First Visit Off','20%'),('Core Services','4')]
    return render(request, 'core/about.html', {'stats': stats})

def contact(request):
    return render(request, 'core/contact.html', {'contact_items': CONTACT_ITEMS})
