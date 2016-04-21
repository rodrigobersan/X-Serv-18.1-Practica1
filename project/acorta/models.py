from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Urls(models.Model):
    longurl = models.CharField(max_length=256)
    shorturl = models.CharField(max_length=128)
