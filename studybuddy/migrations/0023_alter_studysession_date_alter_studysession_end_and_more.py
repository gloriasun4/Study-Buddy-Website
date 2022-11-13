# Generated by Django 4.1.3 on 2022-11-13 22:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("studybuddy", "0022_merge_20221113_2115"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studysession",
            name="date",
            field=models.DateField(default="11-13-2022"),
        ),
        migrations.AlterField(
            model_name="studysession",
            name="end",
            field=models.TimeField(default="23-32"),
        ),
        migrations.AlterField(
            model_name="studysession",
            name="post",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="studybuddy.post",
            ),
        ),
        migrations.AlterField(
            model_name="studysession",
            name="start",
            field=models.TimeField(default="22-32"),
        ),
    ]
