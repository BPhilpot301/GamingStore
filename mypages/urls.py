from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static
from pages import views
from django.contrib.auth import view as auth_views


urlpatterns = [
    path('home/', views.home_view, name="home"),
    path('about/', views.about_view, name="about"),
    path('contact/', views.contact_view, name="contact"),
    path('tourn/', views.tourn_view, name="tourn"),
    path('details/<int:pk>', views.details_view, name="details"),
    path('create/>', views.create_view, name="create"),
]