from django.contrib import admin
from .models import Payment, Order, OrderProduct

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [field.name for field in self.model._meta.fields]
        else:
            return []


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_no','first_name','last_name','email','phone','status','city','order_total')
    inlines = [OrderProductInline]
    

admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
