
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name="root"),
    path('home/', views.home_view, name="home"),
    path('about/', views.about_view, name="about"),
    path('contact/', views.contact_view, name="contact"),
    path('tourn/', views.tourn_view, name="tourn"),
    path('details/<int:pk>', views.details_view, name="details"),
]