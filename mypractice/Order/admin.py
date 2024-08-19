from django.contrib import admin
from Order.models import Order
from OrderItem.models import OrderItem
# Register your models here.

class OrderItemTabularInline(admin.TabularInline):
    model = OrderItem

class Order_admin(admin.ModelAdmin):
    list_display = ('name','email','address','city','state','zip_code','phone','amount','date','payment_id','paid')
    inlines = [OrderItemTabularInline]
admin.site.register(Order,Order_admin)
