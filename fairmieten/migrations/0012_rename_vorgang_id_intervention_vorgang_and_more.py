# Generated by Django 5.1.1 on 2024-10-02 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fairmieten", "0011_rechtsbereich_person_betroffen_item_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="intervention",
            old_name="vorgang_id",
            new_name="vorgang",
        ),
        migrations.AlterField(
            model_name="intervention",
            name="bemerkung",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="intervention",
            name="datum",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="intervention",
            name="form_item",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
