# Generated by Django 5.1.1 on 2024-09-19 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fairmieten", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Charts",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("url", models.CharField(max_length=100)),
                ("description", models.TextField()),
            ],
        ),
    ]