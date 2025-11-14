
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name="home"),
    path('about/', views.about_view, name="about"),
    path('contact/', views.contact_view, name="contact"),
    path('tourn/', views.tourn_view, name="tourn"),
]