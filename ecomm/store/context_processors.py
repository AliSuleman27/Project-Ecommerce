
from .models import Product
from django.db.models import Q

def ram_types(request):
    rams = Product.objects.values_list('ram', flat=True).distinct()
    return dict(rams=rams)

def company_types(request):
    companies = Product.objects.values_list('company', flat=True).distinct()
    return dict(companies=companies)