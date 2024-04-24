from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.



def _get_cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def remove_cart_item_entirely(request,product_id):
    cart    = Cart.objects.get(cart_id=_get_cart_id(request)) 
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')


def remove_cart(request,product_id):
    cart    = Cart.objects.get(cart_id=_get_cart_id(request)) 
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def add_cart(request,product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_get_cart_id(request))
    except Exception as e:
        cart = Cart.objects.create(cart_id = _get_cart_id(request))
        cart.save()
    
    try:
        cart_item = CartItem.objects.get(product=product,cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            cart = cart,
            quantity = 1,
        )
        cart_item.save()

    print("Added To Cart")
    print(f"{product.product_name}")
    print(f"{cart_item.quantity}")
    return redirect('cart')



def cart(request,total=0,quantity=0,cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_get_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,is_active=True)

        if cart_items.count() == 0:
            return render(request,'store/cart.html',context={
                'ZeroItems' : True
            })

        for cart_item in cart_items:
            total = total + cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity

        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context = {
        'cart_items'    :   cart_items,
        'total'         :   total,
        'tax'           :   tax,
        'grand_total'   :   grand_total,
        'quantity'      :   quantity
    }
    return render(request,'store/cart.html',context=context)
        
