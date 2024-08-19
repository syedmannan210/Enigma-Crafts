from django.db import models
from autoslug import AutoSlugField
# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=50)
    des = models.TextField()
    price = models.IntegerField(default=0)
    image = models.FileField(upload_to="product/", max_length=250, null=True, default=None)
    product_slug = AutoSlugField(populate_from='name', unique=True, null=True, default=None)