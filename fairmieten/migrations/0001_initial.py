# Generated by Django 5.1.1 on 2024-09-18 12:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Diskrimminierungsart',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Ergebnis',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Loesungsansaetze',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Diskriminierung',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('typ', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fairmieten.diskrimminierungsart')),
            ],
        ),
        migrations.CreateModel(
            name='Vorgang',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('datum_kontakaufnahme', models.DateField()),
                ('datum_vorfall_von', models.DateField()),
                ('uhrzeit_vorfall', models.TimeField(blank=True, null=True)),
                ('datum_vorfall_bis', models.DateField(blank=True, null=True)),
                ('sprache', models.CharField(max_length=100)),
                ('beschreibung', models.TextField()),
                ('plz', models.IntegerField()),
                ('bezirk_item', models.CharField(max_length=100)),
                ('diskriminierung', models.ManyToManyField(blank=True, to='fairmieten.diskriminierung')),
                ('diskriminierungsart', models.ManyToManyField(blank=True, to='fairmieten.diskrimminierungsart')),
                ('ergebnis', models.ManyToManyField(blank=True, to='fairmieten.ergebnis')),
                ('loesungsansaetze', models.ManyToManyField(blank=True, to='fairmieten.loesungsansaetze')),
            ],
        ),
        migrations.CreateModel(
            name='Intervention',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('datum', models.DateField()),
                ('form_item', models.CharField(max_length=100)),
                ('bemerkung', models.TextField()),
                ('vorgang_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fairmieten.vorgang')),
            ],
        ),
    ]
