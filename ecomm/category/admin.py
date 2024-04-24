from django.contrib import admin
from .models import Category
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name','slug','description']
admin.site.register(Category,CategoryAdmin)