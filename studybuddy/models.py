from django.db import models
from django.conf import settings
import requests
import json

# Create your models here.
class User(models.Model):
    email = models.CharField(primary_key=True, max_length=30, default="")
    firstName = models.CharField(max_length=30, default="")
    lastName = models.CharField(max_length=30, default="")
    zoomLink = models.URLField(max_length=300, default="")
    blurb = models.TextField(default="")
    # implementing friends
    friends = models.ManyToManyField("self")
    username = models.CharField(max_length=30, default="")

# implementing friends
class Friend_Request(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)

class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)

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

    def __str__(self):
        return self.blogname
