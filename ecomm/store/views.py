from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import Product, ReviewRating
from category.models import Category
from carts.models import Cart, CartItem
from carts.views import _get_cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

from .forms import ReviewForm
from orders.models import OrderProduct
from django.contrib import messages


def homepage(request):
    querySet = Product.objects.all().filter(is_available=True)
    context  = {
        'products' : querySet
    }
    return render(request,'home.html',context=context)

def get_related_products(product):
    product_category = product.category
    related_products = Product.objects.filter(category=product_category).exclude(id=product.id)
    related_products = sorted(
        related_products,
        key=lambda p: p.company == product.company,
        reverse=True
    )
    return related_products

def product_detail(request,category_slug,product_slug):
    try:
        single_product  = Product.objects.get(category__slug=category_slug,slug=product_slug)
        is_added        = CartItem.objects.filter(cart__cart_id=_get_cart_id(request),product=single_product).exists()
        reviews         = ReviewRating.objects.filter(product=single_product,status=True).order_by('-created_at')
        if request.user.is_authenticated:
            ordered         = OrderProduct.objects.filter(user=request.user,product=single_product).exists()
        else:
            ordered         = False
        
        recomm = get_related_products(single_product)

    except Exception as e:
        raise e
    context = {
        'single_product'    : single_product,
        'is_added'          : is_added,
        'ordered'           : ordered,
        'reviews'           : reviews,
        'recomm'            : recomm
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
    context = None
    searched_products = None
    product_count = 0
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            searched_products   = Product.objects.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword)).order_by('created_date').distinct()
            product_count       = searched_products.count()
    context = {
        'results'  : product_count,
        'products' : searched_products
    }
    return render(request,"store/store.html",context=context)

def filter(request):

    if request.method == "POST":
        products = Product.objects.all().order_by('created_date')

        ram = request.POST.get('ram')
        company = request.POST.get('company')
        min_price = request.POST.get('min_price')
        max_price = request.POST.get('max_price')

        if ram:
            products = products.filter(ram=ram)
        
        if company:
            products = products.filter(company=company)
        
        if min_price:
            products = products.filter(price__gte=min_price)
        
        if max_price:
            products = products.filter(price__lte=max_price)
        
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

        context = {
            'products' : paged_products,
            'results'  : products.count()
        }

        return render(request,'store/store.html',context=context)

def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return render(request,'base/404.html')
        
        try:
            review = ReviewRating.objects.get(user=request.user,product=product)
            form = ReviewForm(request.POST,instance=review)
            form.save()
            messages.success(request,f'Your review has been updated against {review.product.product_name}')
        
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                rating = form.cleaned_data['rating']
                review = form.cleaned_data['review']
                subject = form.cleaned_data['subject']
                ip = request.META.get('REMOTE_ADDR')
                data = ReviewRating.objects.create(rating=rating,review=review,subject=subject,
                                                   user=request.user,product=product,ip=ip)
                data.save()
                messages.success(request,'Thank You for rating the product')
                
            else:
                messages.warning(request,'Please, Fill Complete the form')

        return redirect(url)
                       