from django.db import models
from django.conf import settings
import requests
import json
import datetime
from django.utils import timezone

# Create your models here.
class User(models.Model):
    email = models.CharField(primary_key=True, max_length=30, default="")
    firstName = models.CharField(max_length=30, default="")
    lastName = models.CharField(max_length=30, default="")
    zoomLink = models.URLField(max_length=300, default="")
    blurb = models.TextField(default="")

class Departments(models.Model):
    dept = models.CharField(max_length = 4)

    def __str__(self):
        return self.dept

class Course(models.Model):
    subject = models.CharField(max_length = 4)
    catalog_number = models.CharField(max_length = 4) #catalog_number = models.CharField(max_length = 4, unique=True)
    instructor = models.CharField(max_length = 30)
    section = models.CharField(max_length = 4)
    course_number = models.CharField(max_length = 10)

    class Meta:
        unique_together = ["subject", "catalog_number", "instructor", "section", "course_number"]

    def __str__(self):
        course_level = self.subject + self.catalog_number
        if(self.instructor == '-'):
            inst = "Not available"
        else:
            inst = self.instructor
        instructor = "Instructor: " + inst
        section = "(Section: " + self.section + ")"
        return course_level + " \n " + instructor + " \n " + section

class Post(models.Model):
    """
    Foreign Key means: one post can only be related to more than one course
    we want this so we can relate posts to more than one section

    Note: change to models.OneToOneField if we want to have a post only be related to one course

    Source for on_delete: https://stackoverflow.com/questions/38388423/what-does-on-delete-do-on-django-models
        we want to remove posts related to the course and/or user when a post is delete, so we are using using CASCADE
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE,)
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    author = models.CharField(max_length = 30, default="Author of this post chose to be anonymous")
    topic = models.CharField(max_length = 30, default="No topic was provided by the author of this post")
    startDate = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    endDate = models.DateField(default=(timezone.now() + datetime.timedelta(days=7)).strftime("%Y-%m-%d"))
    description = models.TextField(default="No description was provided by the author of this post")

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.endDate <= now

    def __str__(self):
        author = "Author: " + self.author
        if type(self.startDate) != str:
            time_frame = "Time Frame: " + self.startDate.strftime("%Y-%m-%d") + " to " + self.endDate.strftime("%Y-%m-%d")
        else:
            time_frame = "Time Frame: " + self.startDate + " to " + self.endDate

        return self.topic + '\n' + author + '\n' + time_frame + '\n'