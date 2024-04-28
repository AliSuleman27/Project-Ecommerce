from django.shortcuts import render, HttpResponse, redirect
from carts.models import CartItem
from .models import Order, OrderProduct, Payment
from carts.models import Cart, CartItem
from .forms import OrderForm
import datetime

#confirmation_email_librarires
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import loader

def send_order_mail(request,order):
    user = request.user
    current_site = get_current_site(request)
    mail_subject = 'Thank you for placing Order'
    message = loader.render_to_string(
        'orders/order_confirmation.html',
        {
            'user'          : user,
            'domain'        : current_site,
            'order'         : order
        }
    )
    to_email = user.email
    send_email = EmailMessage(mail_subject,message,to=[to_email])
    send_email.content_subtype = 'html'
    send_email.send()


def confirm_order(request):
    order = Order.objects.filter(user=request.user,is_ordered=False)
    if order.exists():
        order = order[0]
    payment = Payment.objects.create(
        user = request.user,
        payment_id = order.order_no,
        payment_method = "COD",
        amount_paid = order.order_total,
        status = "Pending",
    )
    order.is_ordered = True
    order.payment = payment
    order.save()

    # Get the Cart and Remove the items
    cart_items = CartItem.objects.filter(user=request.user,is_active=True)
    for item in cart_items:
        product = OrderProduct(
            order = order,
            payment = payment,
            user = request.user,
            product = item.product,
            qunatity = item.quantity,
            product_price = item.product.price,
        )
        product.save()
        #Decerement the Stock Qunatity
        item.product.stock -= item.quantity
        item.delete()
    payment.save()
    
    # Send the Email
    send_order_mail(request,order)
    return redirect('store')

def place_order(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    if cart_items.count() <= 0:
        return redirect('store')

    tax = 0
    grand_total = 0
    quantity = 0
    total = 0
    for cart_item in cart_items:
        total = total + cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity

    tax = 300
    grand_total = total + tax

    print(grand_total)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order.objects.filter(user=user, is_ordered=False)
            if data.exists():
                data = data[0]
            else:
                data = Order()
            
            data.user = user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.addressLine1 = form.cleaned_data['addressLine1']
            data.addressLine2 = form.cleaned_data['addressLine2']
            data.country = form.cleaned_data['country']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')

            data.save()

            year = int(datetime.date.today().strftime("%Y"))
            day = int(datetime.date.today().strftime("%d"))
            month = int(datetime.date.today().strftime('%m'))
            date = datetime.date(year,month,day)
            today = date.strftime('%Y%m%d')
            order_no = today + str(data.id)
            data.order_no = order_no
            print('orderno : ' , order_no)
            data.save()

            context = {
                'order' : data,
                'total' : total,
                'cart_items' : cart_items,
                
            }
            return render(request,'orders/payments.html',context=context)
        else:
            return redirect('checkout')
    else:
        return HttpResponse("Response Recorded")

