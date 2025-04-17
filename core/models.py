from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.IntegerField()
    rating = models.FloatField()
    num_reviews = models.IntegerField()
    image = models.ImageField(upload_to='products/')
    is_bestseller = models.BooleanField(default=False)
    shades_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    

    
from django.utils import timezone

class MobileOTP(models.Model):
    mobile_number = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.mobile_number

from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart ({self.user or self.session_key})"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.product.price

