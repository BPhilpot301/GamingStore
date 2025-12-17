from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Card

from .models import Card, Cart, CartItem


class CardList(ListView):
    model = Card
    template_name = "catalog/list.html"


@login_required
@require_POST
def add_to_cart(request, card_id):
    card = get_object_or_404(Card, id=card_id)

    cart, created = Cart.objects.get_or_create(
        user=request.user,
        status="open",
        defaults={"total": Decimal("0.00")}
    )

    # add the card to the cart (no duplicates)
    CartItem.objects.get_or_create(cart=cart, card=card)

    # update total (make sure Card has a price field)
    cart.total = sum(item.card.price for item in cart.cartitem_set.all())
    cart.save()

    return redirect("cart")


@login_required
def cart_view(request):
    cart = Cart.objects.filter(user=request.user, status="open").first()
    items = CartItem.objects.filter(cart=cart) if cart else []
    return render(request, "catalog/cart.html", {"cart": cart, "items": items})