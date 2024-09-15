# Generated by Django 5.1.1 on 2024-09-14 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Employee",
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
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("mobile", models.CharField(max_length=15)),
                ("date_of_birth", models.DateField()),
                (
                    "profile_picture",
                    models.ImageField(blank=True, null=True, upload_to="pictures"),
                ),
            ],
        ),
    ]