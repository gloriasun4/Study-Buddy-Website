# Generated by Django 4.1.3 on 2022-11-13 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("studybuddy", "0019_studysession_users_alter_studysession_end_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studysession",
            name="end",
            field=models.TimeField(default="20-05"),
        ),
        migrations.AlterField(
            model_name="studysession",
            name="post",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="studybuddy.post",
            ),
        ),
        migrations.AlterField(
            model_name="studysession",
            name="start",
            field=models.TimeField(default="19-05"),
        ),
    ]
