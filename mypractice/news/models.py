from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField
# Create your models here.
class News(models.Model):
    news_title=models.CharField(max_length=80)
    news_des=HTMLField()
    news_slug = AutoSlugField(populate_from='news_title', unique=True,null=True,default=None)