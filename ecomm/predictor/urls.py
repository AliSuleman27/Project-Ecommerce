from django.urls import path
from .views import *
urlpatterns = [
    path('predict/',predict,name='predict'),
]