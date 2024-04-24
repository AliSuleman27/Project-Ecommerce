from django.contrib import admin
from .models import Product

# Register your models here.
# class ProductImageInLine(admin.StackedInline):
#     model = ProductImage
#     extra = 1


# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('product_name','price','stock','category','is_available','created_date','modified_date')
#     inlines = [ProductImageInLine]


# admin.site.register(Inventory)
admin.site.register(Product)