from django.shortcuts import render, HttpResponse, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

#verification_email_librarires
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Cart Session key
from carts.views import _get_cart_id
from carts.models import Cart, CartItem

# Order Models
from orders.models import Order, OrderProduct

# Create your views here., 

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email,password=password)
        if user:
            cart = None
            try:
                cart_id = _get_cart_id(request)
                print(cart_id)
                cart = Cart.objects.get(cart_id=cart_id)
                cart_items_local = CartItem.objects.filter(cart=cart)
                cart_items_user =  CartItem.objects.filter(user=user)
                if cart_items_local.exists():
                    for item in cart_items_local:
                        obj = cart_items_user.filter(product=item.product)
                        if obj.exists():
                            print('overlapped ',obj[0].product.product_name)
                            item.quantity += obj[0].quantity
                            obj[0].delete()
                        item.user = user
                        item.save()
            except:
                pass
            auth.login(request,user)
            messages.success(request,"Login Success.")
            return redirect('dashboard')
        else:
            messages.warning(request,"Invalid Login Credentials")
            return redirect('login')
    return render(request,'accounts/login.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,"Logged out Successfully")
    return redirect('login')


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            phone_number = form.cleaned_data['phone_number']

            username = email.split('@')[0]
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,
                                               email=email,password=password,username=username,
                                               )
            user.phone_number = phone_number
            user.save()
        

            # Verification of User
            current_site = get_current_site(request)
            mail_subject = 'Please Activate Your Account'
            message = render_to_string(
                'accounts/account_activation_email.html',
                {
                    'user'          : user,
                    'domain'        : current_site,
                    'uid'           : urlsafe_base64_encode(force_bytes(user.pk)),
                    'token'         : default_token_generator.make_token(user),
                }
            )
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            return redirect('/accounts/login/?command=verification&Email='+email)
    else:  
        form = RegistrationForm()
    context = {
        'form' : form
    }
    return render(request,'accounts/register.html',context)

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    token_verified = default_token_generator.check_token(user=user,token=token)
    if user and token_verified:
        user.is_active = True
        user.save()
        messages.success(request,"Congratulations! Account Activated Successfully.")
        return redirect('login')
    else:
        messages.warning(request,"Invalid Activation Link, \nAn email is sent on your email, verify using that.")
        return redirect('register')

@login_required(login_url = 'login')
def dashboard(request):
    user = request.user
    orders = Order.objects.filter(user=user,is_ordered=True)
    context = {
        'order_count' : orders.count()
    }
    return render(request,'accounts/dashboard.html',context=context)

@login_required(login_url = 'login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders' : orders,
        'order_count' : orders.count()
    }
    return render(request,'accounts/my_orders.html',context=context)

@login_required(login_url = 'login')
def change_password(request):
    if request.method == "POST":
        user = request.user
        current_passowrd = request.POST['current']
        new_pass0 = request.POST['password0']
        new_pass1 = request.POST['password0']

        account = Account.objects.get(id=user.id)
        if account.check_password(current_passowrd):
            if new_pass0 == new_pass1:
                if len(new_pass0) < 8:
                    messages.warning(request,"Password is too short")
                else:
                    account.set_password(new_pass1)
                    account.save()
                    messages.success(request,"Password Changed Successfully")
            else:
                messages.warning(request,"Password did not match")
        else:
                messages.warning(request,"Invalid Old Password")
        return redirect('change_password')
    return render(request,'accounts/changePassword.html')

def forgotPassword(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = Account.objects.filter(email=email)
        if user.exists():
            user = user[0]
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Account Password'
            message = render_to_string(
                'accounts/account_forgot_password_email.html',
                {
                    'user'          : user,
                    'domain'        : current_site,
                    'uid'           : urlsafe_base64_encode(force_bytes(user.pk)),
                    'token'         : default_token_generator.make_token(user),
                }
            )
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'An Email has been sent on your account. Please verify.')
            return redirect('login')

        else:
            messages.warning(request,"Account doesn't Exist!")
            redirect('forgotPassword')

    return render(request,'accounts/forgotPassword.html')

def resetPassword_link_validation(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    token_verified = default_token_generator.check_token(user=user,token=token)
    if user and token_verified:
        request.session['uid'] = uid
        messages.success(request,"Please reset your password")
        return redirect('resetPassword')
    else:
        messages.warning(request,"Invalid Activation Link, \nAn email is sent on your email, validate using that.")
        return redirect('login')

def resetPassword(request):
    if request.method == "POST":
        password0 = request.POST.get('password0')
        password1 = request.POST.get('password1')
        if password0 == password1:
            user = Account.objects.get(pk=request.session['uid'])
            user.set_password(password1)
            user.save()
            messages.success(request,"Password Changed Successfully")
            return redirect('login')
        else:
            messages.warning(request,"Password Didn't Matched....")
            return redirect('resetPassword')

    return render(request,'accounts/resetPassword.html')