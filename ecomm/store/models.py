from django.db import models
from category.models import Category
from django.utils.text import slugify
from django.urls import reverse


class Product(models.Model):
    product_name        = models.CharField(max_length=200, unique=True)
    slug                = models.SlugField(unique=True,blank=True)
    description         = models.TextField(max_length=500, blank=True)
    ram                 = models.IntegerField(blank=True,null=True)
    storage             = models.CharField(max_length=300,blank=True,null=True)
    screen_size         = models.CharField(max_length=200,blank=True,null=True)
    processer           = models.CharField(max_length=300,blank=True,null=True)
    GPU                 = models.CharField(max_length=200,blank=True,null=True)
    OS                  = models.CharField(max_length=100,blank=True,null=True)
    weight              = models.FloatField(blank=True,null=True)
    touchscreen         = models.BooleanField(default=False,blank=True)
    IPS                 = models.BooleanField(default=False,blank=True)
    price               = models.IntegerField()
    stock               = models.IntegerField(default=0)
    is_available        = models.BooleanField(default=True)
    category            = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    created_date        = models.DateTimeField(auto_now_add=True)
    modified_date       = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.product_name
    
    def save(self,*args,**kwargs):
        self.slug = slugify(self.product_name)
        super(Product,self).save(*args,**kwargs)
    
    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])



# class Inventory(models.Model):
#     inventory_date          = models.DateField(auto_now_add=True)
#     product                 = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_inventory')
#     quantity                = models.IntegerField()
#     unit_price              = models.IntegerField()
#     actual_value            = models.IntegerField(default=0)
#     expected_profit_value   = models.IntegerField(default=0)

#     def __str__(self) -> str:
#         return self.product.product_name
    
#     def save(self,*args,**kwargs):
#         self.expected_profit_value  = self.quantity * self.product.price
#         self.actual_value           = self.quantity * self.unit_price    
#         obj = Product.objects.get(slug=self.product.slug)
#         obj.stock += self.quantity
#         obj.save()
#         super(Inventory,self).save(*args,**kwargs)


class ProductImage(models.Model):
    product             = models.ForeignKey(Product,on_delete=models.Case,related_name='product_images') 
    image               = models.ImageField(upload_to='products')

