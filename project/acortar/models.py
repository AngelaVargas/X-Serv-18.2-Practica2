from django.db import models

# Create your models here.

class urls(models.Model):
    longer = models.CharField(max_length=28)
    short = models.CharField(max_length=28)
