from django.contrib import admin
from Contact.models import Contact
# Register your models here.

class Contact_admin(admin.ModelAdmin):
    list_display = ('name','email','phone','date','message')

admin.site.register(Contact,Contact_admin)