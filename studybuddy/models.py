from django.db import models

# Create your models here.
class User(models.Model):

    email = models.CharField(primary_key=True)
    username = models.CharField(max_length=30)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    zoomLink = models.URLField()
    blurb = models.TextField()
