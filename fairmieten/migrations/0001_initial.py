# Generated by Django 5.1.1 on 2024-11-04 11:13

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models
from django.contrib.auth.models import User
import os
from fairmieten.insert_initial_data import setup


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# fairmieten.migrations.0018_create_superuser

def create_superuser(apps, schema_editor):
    # Umgebungsvariablen abrufen
    username = os.getenv('ADMIN_USERNAME', 'admin')
    password = os.getenv('ADMIN_PASSWORD', 'adminpassword')
    email = os.getenv('ADMIN_EMAIL', 'admin@example.com')

    # Superuser nur erstellen, wenn er nicht bereits existiert
    print("Search for ", username)
    user = User.objects.filter(username=username)
    print("User: ", user)
    if not user.exists():
        print("Create Superuser")
        User.objects.create_superuser(username=username, email=email, password=password)


class Migration(migrations.Migration):

    initial = True
    
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Diskrimminierungsart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Ergebnis',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Loesungsansaetze',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Diskriminierung',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('typ', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fairmieten.diskrimminierungsart')),
            ],
        ),
        migrations.CreateModel(
            name='Vorgang',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('datum_kontakaufnahme', models.DateField(blank=True, null=True)),
                ('datum_vorfall_von', models.DateField(blank=True, null=True)),
                ('datum_vorfall_bis', models.DateField(blank=True, null=True)),
                ('sprache', models.CharField(max_length=100)),
                ('beschreibung', models.TextField(blank=True, null=True)),
                ('bezirk_item', models.CharField(max_length=100)),
                ('diskriminierung', models.ManyToManyField(blank=True, to='fairmieten.diskriminierung')),
                ('ergebnis', models.ManyToManyField(blank=True, to='fairmieten.ergebnis')),
                ('loesungsansaetze', models.ManyToManyField(blank=True, to='fairmieten.loesungsansaetze')),
                ('fallnummer', models.IntegerField(blank=True, null=True)),
                ('kontakaufnahme_durch_item', models.CharField(blank=True, max_length=100, null=True)),
                ('vorgangstyp_item', models.CharField(blank=True, max_length=100, null=True)),
                ('zugang_fachstelle_item', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Intervention',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('datum', models.DateField(blank=True, null=True)),
                ('form_item', models.CharField(blank=True, max_length=100, null=True)),
                ('bemerkung', models.TextField(blank=True, null=True)),
                ('vorgang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fairmieten.vorgang')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Verursacher',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('unternehmenstyp_item', models.CharField(max_length=100)),
                ('personentyp_item', models.CharField(max_length=100)),
                ('vorgang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fairmieten.vorgang')),
            ],
        ),
        migrations.CreateModel(
            name='Rechtsbereich',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='vorgang',
            name='rechtsbereich',
            field=models.ManyToManyField(blank=True, to='fairmieten.rechtsbereich'),
        ),
        migrations.RenameField(
            model_name='vorgang',
            old_name='datum_kontakaufnahme',
            new_name='datum_kontaktaufnahme',
        ),
        migrations.RenameField(
            model_name='vorgang',
            old_name='kontakaufnahme_durch_item',
            new_name='kontaktaufnahme_durch_item',
        ),
        migrations.AlterField(
            model_name='vorgang',
            name='bezirk_item',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vorgang',
            name='sprache',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
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
            name='Person',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('alter_item', models.CharField(max_length=100)),
                ('anzahl_kinder', models.IntegerField(blank=True, null=True)),
                ('gender_item', models.CharField(max_length=100)),
                ('vorgang', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fairmieten.vorgang')),
                ('betroffen_item', models.CharField(blank=True, max_length=100, null=True)),
                ('prozeskostenuebernahme_item', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FormValues',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('model', models.CharField(choices=[], default=None, max_length=100)),
                ('field', models.CharField(default=None, max_length=100)),
                ('value', models.CharField(max_length=100)),
                ('key', models.CharField(blank=True, default=None, max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='vorgang',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunPython(
            code=create_superuser,
        ),
        migrations.AddField(
            model_name='vorgang',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vorgang',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='vorgang',
            name='loesungsansaetze_bemerkung',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vorgang',
            name='ergebnis_bemerkung',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Diskriminierungsform',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='bereich_diskriminierung_item',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='formvalues',
            name='encoding',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='person',
            name='diskriminierungsform',
            field=models.ManyToManyField(blank=True, to='fairmieten.diskriminierungsform'),
        ),
        migrations.RunPython(
            code=setup,
        ),
    ]
