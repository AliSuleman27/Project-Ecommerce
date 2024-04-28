from django.urls import path
from .views import place_order, confirm_order
urlpatterns = [
    path('place_order/',place_order,name='place_order'),
    path('confirm_order/',confirm_order,name='confirm_order'),
]