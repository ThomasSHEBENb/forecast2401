from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
]