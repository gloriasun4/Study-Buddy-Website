# Generated by Django 4.1.3 on 2022-11-14 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("studybuddy", "0024_alter_post_enddate_alter_post_startdate_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="studysession",
            name="author",
            field=models.CharField(default="admin", max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="studysession",
            name="end",
            field=models.TimeField(default="19-50"),
        ),
        migrations.AlterField(
            model_name="studysession",
            name="start",
            field=models.TimeField(default="18-50"),
        ),
    ]
