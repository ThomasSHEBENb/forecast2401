from django.urls import path, re_path
from .views import main, about, contact

urlpatterns = [
    path('', about, name = 'about'),
    re_path(r'^main', main, name='index'),
    re_path(r'^contact', contact, name = 'contact')
]
