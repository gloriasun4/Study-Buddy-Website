# Generated by Django 4.1.1 on 2022-11-06 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("studybuddy", "0002_course_departments"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="major",
            field=models.CharField(default="", max_length=30),
        ),
        migrations.AddField(
            model_name="user",
            name="name",
            field=models.CharField(default="", max_length=50),
        ),
    ]
