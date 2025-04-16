from django.urls import path
from . import views
from .views import google_login_redirect
from django.contrib.auth.views import LogoutView




urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('sign-in-mobile/', views.sign_in_mobile, name='sign_in_mobile'),  # Sign-in page
    path('makeup-store/', views.makeup_store, name='makeup_store'),
    path('gift_cards/', views.gift_cards, name='gift_cards'),
    path('corporate/', views.corporate, name='corporate'), 
    path('how-to-use/', views.how_to_use, name='how_to_use'),
    path('terms-conditions/', views.terms_conditions, name='terms_conditions'),
    path('baby/', views.baby, name='baby'),
    path('login/google-direct/', google_login_redirect, name='google_direct_login'),
    path('diapers/', views.diapers_page, name='diapers'),
    path('wipes/', views.wipes_page, name='wipes'),
    path('babypowder/', views.babypowder_page, name='babypowder'),
    path('babyoils/', views.babyoils_page, name='babyoils'),
    path('bodywash/', views.bodywash_page, name='bodywash'),
    path('makeup-products/', views.makeup_products, name='makeup_products'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
   
]