from django.urls import path
from .views import *
urlpatterns = [
    path('',cart,name='cart'),
    path('add_cart/<int:product_id>/',add_cart,name="add_cart"),
    path('remove_cart/<int:product_id>/',remove_cart,name="remove_cart"),
    path('remove_cart_item_entirely/<int:product_id>/',remove_cart_item_entirely,name="remove_cart_item_entirely"),
    path('checkout/',checkout,name="checkout"),
]