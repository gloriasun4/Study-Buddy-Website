from django.db import models

# Create your models here.
class User(models.Model):

    email = models.CharField(primary_key=True, max_length=30, default="")
    #username = models.CharField(max_length=30)
    firstName = models.CharField(max_length=30, default="")
    lastName = models.CharField(max_length=30, default="")
    zoomLink = models.URLField(max_length=300, default="")
    blurb = models.TextField(default="")
