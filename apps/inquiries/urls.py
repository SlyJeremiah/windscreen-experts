from django.urls import path
from . import views

urlpatterns = [
    path('', views.inquiry_create, name='inquiry_create'),
    path('success/', views.inquiry_success, name='inquiry_success'),
]
