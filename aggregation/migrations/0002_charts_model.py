# Generated by Django 5.1.1 on 2024-10-02 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aggregation", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="charts",
            name="model",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
