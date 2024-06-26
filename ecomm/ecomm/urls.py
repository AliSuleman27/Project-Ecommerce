
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from store.views import homepage
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homepage,name="homepage"),
    path('store/',include('store.urls')),
    path('cart/',include('carts.urls')),
    path('accounts/',include('accounts.urls')),
    path('orders/',include('orders.urls')),
    path('predictor/',include('predictor.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

