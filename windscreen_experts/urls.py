from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('services/', include('apps.services.urls')),
    path('bookings/', include('apps.bookings.urls')),
    path('gallery/', include('apps.gallery.urls')),
    path('inquiries/', include('apps.inquiries.urls')),
    path('admin-panel/', include('apps.core.admin_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
