from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home',views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'), 
    path('privacy', views.privacy, name='privacy'),
    path('terms', views.terms, name='terms'),
    path('summary', views.summary, name='summary'),
    path('gallery', views.gallery, name='gallery'),
    path('doctors', views.doctors, name='doctors'),
    path('appointment', views.appointment, name='appointment'),
]