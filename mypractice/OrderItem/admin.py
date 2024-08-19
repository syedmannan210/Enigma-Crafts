from django.contrib import admin
from OrderItem.models import OrderItem
# Register your models here.
class OrderItem_admin(admin.ModelAdmin):
    list_display = ('user','order','product','image','quantity','price','total')
admin.site.register(OrderItem,OrderItem_admin)







