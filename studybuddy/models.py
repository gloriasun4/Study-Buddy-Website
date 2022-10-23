from django.db import models
from django.conf import settings
import requests
import json

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

class Departments(models.Model):
    dept = models.CharField(max_length = 4)

    def __str__(self):
        return self.dept

class Course(models.Model):
    subject = models.CharField(max_length = 4)
    catalog_number = models.CharField(max_length = 4)
    instructor = models.CharField(max_length = 30)
    section = models.CharField(max_length = 4)
    course_number = models.CharField(max_length = 10)

    def __str__(self):
        course_level = self.subject + self.catalog_number
        if(self.instructor == '-'):
            inst = "Not available"
        else:
            inst = self.instructor
        instructor = "Instructor: " + inst
        section = "(Section: " + self.section + ")"
        return course_level + " \n " + instructor + " \n " + section


from django.db import models
# User = settings.AUTH_USER_MODEL

# Create your models here.
class Snippet(models.Model):
    user = models.ForeignKey(User,
                             default=1,
                             null=True,
                             on_delete=models.SET_NULL
                             )
    blogname = models.CharField(max_length=100)
    blogauth = models.CharField(max_length=100)
    blogdes = models.TextField(max_length=400)
    img = models.ImageField(upload_to='pics')

    def __str__(self):
        return self.blogname