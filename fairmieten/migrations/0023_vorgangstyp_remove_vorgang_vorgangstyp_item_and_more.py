# Generated by Django 5.1.2 on 2024-11-04 11:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fairmieten', '0022_formvalues_encoding'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vorgangstyp',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='vorgang',
            name='vorgangstyp_item',
        ),
        migrations.AlterField(
            model_name='formvalues',
            name='encoding',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vorgang',
            name='vorgangstyp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fairmieten.vorgangstyp'),
        ),
    ]