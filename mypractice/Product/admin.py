from django.contrib import admin
from Product.models import Product
# Register your models here.
class Product_Admin(admin.ModelAdmin):
    list_display = ('name','des','price','image')
admin.site.register(Product,Product_Admin)