from django.contrib import admin
from service.models import service
# Register your models here.
class Service_Admin(admin.ModelAdmin):
    list_display = ('service_title','service_des','service_image')
admin.site.register(service,Service_Admin)