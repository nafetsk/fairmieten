# Generated by Django 5.1.2 on 2024-11-21 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("fairmieten", "0005_vorgang_ander_sprache"),
    ]

    operations = [
        migrations.RenameField(
            model_name="vorgang",
            old_name="ander_sprache",
            new_name="andere_sprache",
        ),
    ]
