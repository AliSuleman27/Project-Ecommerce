from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Product
from category.models import Category
from carts.models import Cart, CartItem
from carts.views import _get_cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator




def homepage(request):
    querySet = Product.objects.all().filter(is_available=True)
    context  = {
        'products' : querySet
    }
    return render(request,'home.html',context=context)

def product_detail(request,category_slug,product_slug):
    try:
        single_product  = Product.objects.get(category__slug=category_slug,slug=product_slug)
        is_added        = CartItem.objects.filter(cart__cart_id=_get_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e
    context = {
        'single_product'    : single_product,
        'is_added'          : is_added
    }
    return render(request,'store/product_detail.html',context=context)

def store(request,category_slug=None):
    category = None
    products = None
    product_count = 0

    if category_slug != None:
        category = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(category=category,is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

    product_count  = products.count()
    context = {
        'results'  : product_count,
        'products' : paged_products
    }
    return render(request,"store/store.html",context=context)

def search(request):
    return render(request,"store/store.html")