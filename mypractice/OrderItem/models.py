from django.db import models
from django.contrib.auth.models import User
from Order.models import Order
# Create your models here.
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.CharField(max_length=90)
    image=models.FileField(upload_to="product/")
    quantity=models.CharField(max_length=20)
    price=models.CharField(max_length=50)
    total=models.CharField(max_length=1000)

def __str__(self):
    return self.order.user.username
