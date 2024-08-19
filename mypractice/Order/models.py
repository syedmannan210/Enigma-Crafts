from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    order_id= models.AutoField(primary_key=True, unique=True)
    name=models.CharField(max_length=90)
    email=models.CharField(max_length=111)
    address=models.CharField(max_length=111)
    city=models.CharField(max_length=111)
    state=models.CharField(max_length=111)
    zip_code=models.CharField(max_length=111, default="")
    phone=models.CharField(max_length=13, default="")
    amount=models.CharField(max_length=100)
    date=models.DateField(auto_now_add=True)
    payment_id=models.CharField(max_length=100,null=True,blank=True)
    paid=models.BooleanField(default=False,null=True)

def __str__(self):
    return self.user.username
