from catalog.models import Cart, CartItem

def cart_item_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            count = sum(item.quantity for item in CartItem.objects.filter(cart=cart))
        else:
            count = 0
    else:
        count = 0

    return {
        'cart_item_count':count
    }