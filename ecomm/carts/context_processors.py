
from .models import Cart,CartItem
from .views import _get_cart_id

def counter(request):
    count = 0
    if 'admin' in request.path:
        return {}
    else:
        cart_items = None
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user = request.user, is_active=True)
        else:
            cart = Cart.objects.filter(cart_id=_get_cart_id(request))
            if cart.exists():
                cart_items = CartItem.objects.filter(cart=cart[0])
        
        if cart_items:
            for item in cart_items:
                count += item.quantity
        return dict(cart_count=count)