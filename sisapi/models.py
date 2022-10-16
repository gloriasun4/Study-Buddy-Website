from django.db import models


class Instructor(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=30, unique=True)


class Section(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    course_number = models.IntegerField(unique=True)
    semester_code = models.IntegerField()
    course_section = models.TextField(max_length=3)
    subject = models.TextField(max_length=4)
    catalog_number = models.TextField(max_length=6)
    description = models.TextField(max_length=100)
    units = models.TextField(max_length=10)
    component = models.TextField(max_length=3)
    class_capacity = models.IntegerField()
    wait_list = models.IntegerField()
    wait_cap = models.IntegerField()
    enrollment_total = models.IntegerField()
    enrollment_available = models.IntegerField()
    topic = models.TextField(blank=True, null=True)


class Meeting(models.Model):
    section = models.ForeignKey(Section, related_name='meetings', on_delete=models.CASCADE)
    days = models.TextField(max_length=10)
    start_time = models.TextField(max_length=21)
    facility_description = models.TextField(max_length=50)
    end_time = models.TextField(max_length=21)

