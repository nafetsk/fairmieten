# Generated by Django 5.1.1 on 2024-10-06 07:16

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fairmieten', '0012_alter_vorgang_bezirk_item_alter_vorgang_sprache'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormLabels',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('model', models.CharField(choices=[], default=None, max_length=100)),
                ('field', models.CharField(default=None, max_length=100)),
                ('label', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FormValues',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('model', models.CharField(choices=[], default=None, max_length=100)),
                ('field', models.CharField(default=None, max_length=100)),
                ('value', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='person',
            name='vorgang',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fairmieten.vorgang'),
        ),
    ]