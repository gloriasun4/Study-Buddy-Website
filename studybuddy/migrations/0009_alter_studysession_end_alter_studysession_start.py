# Generated by Django 4.1.3 on 2022-11-08 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("studybuddy", "0008_studysession_accepted_alter_studysession_end_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studysession",
            name="end",
            field=models.TimeField(default="06-35"),
        ),
        migrations.AlterField(
            model_name="studysession",
            name="start",
            field=models.TimeField(default="05-35"),
        ),
    ]
