# Generated by Django 5.1.1 on 2024-09-19 21:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("fairmieten", "0002_charts"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="charts",
            name="description",
        ),
    ]
