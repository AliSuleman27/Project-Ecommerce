from django.db import models
from store.models import Product
from accounts.models import Account
# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)
    def __str__(self) -> str:
        return self.cart_id
    
class CartItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True,blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.product_name 

    def sub_total(self):
        return self.product.price * self.quantity
