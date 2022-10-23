# Generated by Django 4.1.1 on 2022-10-23 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("subject", models.CharField(max_length=4)),
                ("catalog_number", models.CharField(max_length=4)),
                ("instructor", models.CharField(max_length=30)),
                ("section", models.CharField(max_length=4)),
                ("course_number", models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="Departments",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("dept", models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=30)),
                ("password", models.CharField(max_length=30)),
            ],
        ),
    ]
