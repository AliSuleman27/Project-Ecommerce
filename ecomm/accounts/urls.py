
from django.urls import path
from .views import *
urlpatterns = [
    path('login/',login,name="login"),
    path('register/',register,name="register"),
    path('logout/',logout,name="logout"),
    path('dashboard/',dashboard,name="dashboard"),
    path('',dashboard,name="accounts"),
    path('activate/<uidb64>/<token>/',activate,name='activate'),
    path('forgotPassword/',forgotPassword,name="forgotPassword"),
    path('resetPassword_link_validation/<uidb64>/<token>/',resetPassword_link_validation,name='resetPassword_link_validation'),
    path('resetPassword/',resetPassword,name="resetPassword"),
    path('my_orders/',my_orders,name="my_orders"),
    path('change_password/',change_password,name="change_password"),
]
