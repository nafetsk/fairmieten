# Generated by Django 5.1.1 on 2024-09-23 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fairmieten', '0003_remove_charts_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vorgang',
            name='diskriminierungsart',
        ),
    ]
