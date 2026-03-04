from django.urls import path
from apps.core import admin_views

urlpatterns = [
    path('', admin_views.dashboard, name='admin_dashboard'),
    path('login/', admin_views.admin_login, name='admin_login'),
    path('logout/', admin_views.admin_logout, name='admin_logout'),

    # Bookings
    path('bookings/', admin_views.booking_list, name='admin_bookings'),
    path('bookings/<int:pk>/', admin_views.booking_detail, name='admin_booking_detail'),
    path('bookings/<int:pk>/delete/', admin_views.booking_delete, name='admin_booking_delete'),

    # Gallery
    path('gallery/', admin_views.gallery_list, name='admin_gallery'),
    path('gallery/add/', admin_views.gallery_add, name='admin_gallery_add'),
    path('gallery/<int:pk>/edit/', admin_views.gallery_edit, name='admin_gallery_edit'),
    path('gallery/<int:pk>/delete/', admin_views.gallery_delete, name='admin_gallery_delete'),

    # Services
    path('services/', admin_views.service_list, name='admin_services'),
    path('services/add/', admin_views.service_add, name='admin_service_add'),
    path('services/<int:pk>/edit/', admin_views.service_edit, name='admin_service_edit'),
    path('services/<int:pk>/delete/', admin_views.service_delete, name='admin_service_delete'),

    # Inquiries
    path('inquiries/', admin_views.inquiry_list, name='admin_inquiries'),
    path('inquiries/<int:pk>/', admin_views.inquiry_detail, name='admin_inquiry_detail'),

    # Customers
    path('customers/', admin_views.customer_list, name='admin_customers'),
]
