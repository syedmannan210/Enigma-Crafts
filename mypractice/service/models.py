from django.db import models

# Create your models here.
class service(models.Model):
    service_des=models.TextField()
    service_image=models.FileField(upload_to="ourservices/",max_length=250,null=True, default=None)
    service_title=models.CharField(max_length=50)