# Generated by Django 4.1.3 on 2022-11-13 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("studybuddy", "0016_alter_room_post_alter_studysession_end_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="studysession",
            name="post",
            field=models.OneToOneField(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="studybuddy.post",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="studysession",
            name="end",
            field=models.TimeField(default="19-17"),
        ),
        migrations.AlterField(
            model_name="studysession",
            name="start",
            field=models.TimeField(default="18-17"),
        ),
    ]