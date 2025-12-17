from django.urls import path
from . import views

urlpatterns = [
    path("", views.CardList.as_view(), name="card_list"),
    path("add_to_cart/<int:card_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_view, name="cart"),
]

