# Generated by Django 5.1.1 on 2024-09-27 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fairmieten", "0006_remove_charts_name_remove_charts_url_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="charts",
            name="name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
