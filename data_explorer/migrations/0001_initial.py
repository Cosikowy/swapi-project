# Generated by Django 4.1.7 on 2023-02-24 03:09

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Collection",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        primary_key=True, serialize=False, verbose_name="Collection ID"
                    ),
                ),
                (
                    "file_name",
                    models.CharField(max_length=72, verbose_name="File Name"),
                ),
                ("file_location", models.TextField(verbose_name="File Location")),
                (
                    "timestamp",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Download timestamp"
                    ),
                ),
                ("etag", models.CharField(max_length=80, verbose_name="Version tag")),
                ("endpoint", models.CharField(max_length=50, verbose_name="Endpoint")),
            ],
        ),
    ]