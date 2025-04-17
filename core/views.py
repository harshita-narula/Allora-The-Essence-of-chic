from django.shortcuts import render
from .models import Product

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.models import SocialApp
from django.conf import settings


def google_login_redirect(request):
    app = SocialApp.objects.get(provider='google')
    client_id = app.client_id
    redirect_uri = request.build_absolute_uri('/accounts/google/login/callback/')

    scope = "email profile"
    oauth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={client_id}"
        f"&response_type=code"
        f"&scope={scope}"
        f"&redirect_uri={redirect_uri}"
        f"&state=custom_state"
        f"&access_type=online"
        f"&prompt=select_account"
    )
    return redirect(oauth_url)


import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, get_backends
from django.contrib.auth.models import User
from .models import MobileOTP
from .forms import MobileNumberForm, OTPForm

def send_otp(request):
    if request.method == 'POST':
        form = MobileNumberForm(request.POST)
        if form.is_valid():
            mobile = form.cleaned_data['mobile_number']
            otp = str(random.randint(100000, 999999))

            # Save or update OTP
            MobileOTP.objects.update_or_create(
                mobile_number=mobile,
                defaults={'otp': otp}
            )

            print(f"OTP for {mobile} is {otp}")  

            request.session['mobile'] = mobile
            return redirect('verify_otp')
    else:
        form = MobileNumberForm()
    
    return render(request, 'send_otp.html', {'form': form})


def verify_otp(request):
    mobile = request.session.get('mobile')
    if not mobile:
        return redirect('send_otp')

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            try:
                otp_obj = MobileOTP.objects.get(mobile_number=mobile, otp=entered_otp)
                
                # Get or create user
                user, created = User.objects.get_or_create(username=mobile)

                # Tell Django which backend to use
                backend = get_backends()[0]
                user.backend = backend.__module__ + '.' + backend.__class__.__name__

                login(request, user)

                return redirect('index') 
            except MobileOTP.DoesNotExist:
                form.add_error('otp', 'Invalid OTP')
    else:
        form = OTPForm()

    return render(request, 'verify_otp.html', {'form': form})




from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')

def sign_in_mobile(request):
    return render(request, 'sign-in-mobile.html')

def makeup_store(request):
    return render(request, 'makeup.html')

def gift_cards(request):
    return render(request, 'gift_cards.html') 

def corporate(request):
    return render(request, 'corporate_gift_cards.html')

def how_to_use(request):
    return render(request, 'how_to_use.html')

def terms_conditions(request):
    return render(request, 'terms.html')

def baby(request):
    return render(request, 'baby.html')

def diapers_page(request):
    return render(request, 'diapers.html')

def wipes_page(request):
    return render(request, 'wipes.html')

def babypowder_page(request):
    return render(request, 'babypowder.html')
    
def babyoils_page(request):
    return render(request, 'babyoils.html')

def bodywash_page(request):
    return render(request, 'bodywash.html')

from django.db.models import Q
from django.core.paginator import Paginator

def makeup_products(request):
    query = request.GET.get('q', '')
    selected_brands = request.GET.getlist('brand')
    selected_categories = request.GET.getlist('category')
    selected_price = request.GET.get('price')

    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(category__icontains=query)
        )
    if selected_brands:
        products = products.filter(brand__in=selected_brands)
    if selected_categories:
        products = products.filter(category__in=selected_categories)
    if selected_price:
        if selected_price == '0-250':
            products = products.filter(discounted_price__lte=250)
        elif selected_price == '251-500':
            products = products.filter(discounted_price__gt=250, discounted_price__lte=500)
        elif selected_price == '501-1000':
            products = products.filter(discounted_price__gt=500, discounted_price__lte=1000)

    
    paginator = Paginator(products, 9) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj.object_list, 
        'page_obj': page_obj,
        'query': query,
        'selected_brands': selected_brands,
        'selected_categories': selected_categories,
        'selected_price': selected_price,
    }

    return render(request, 'makeup_products.html', context)