# Generated by Django 5.1.1 on 2024-11-11 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("fairmieten", "0002_vorgang_alter_item_vorgang_anzahl_kinder_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="vorgang",
            old_name="sprache",
            new_name="sprache_item",
        ),
    ]