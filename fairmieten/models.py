from math import e
import uuid
from django.db import models
from django.apps import apps


class Diskrimminierungsart(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Diskriminierung(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    name = models.CharField(max_length=100)
    typ = models.ForeignKey(Diskrimminierungsart, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Loesungsansaetze(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Rechtsbereich(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Ergebnis(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Vorgang(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    fallnummer = models.IntegerField(null=True, blank=True)
    vorgangstyp_item = models.CharField(max_length=100, null=True, blank=True) # allgemeine Beratung, Meldung, Fallbetreuung
    datum_kontakaufnahme = models.DateField(null=True, blank=True)
    kontakaufnahme_durch_item = models.CharField(max_length=100, null=True, blank=True) # (Betroffene Person, beschuldigte Person, unbeteiligte Person)
    datum_vorfall_von = models.DateField(null=True, blank=True)
    datum_vorfall_bis = models.DateField(null=True, blank=True)
    sprache = models.CharField(max_length=100, null=True, blank=True)
    beschreibung = models.TextField(null=True, blank=True)
    bezirk_item = models.CharField(max_length=100, null=True, blank=True)
    diskriminierung = models.ManyToManyField(Diskriminierung, blank=True)
    loesungsansaetze = models.ManyToManyField(Loesungsansaetze, blank=True)
    ergebnis = models.ManyToManyField(Ergebnis, blank=True)
    rechtsbereich = models.ManyToManyField(Rechtsbereich, blank=True)
    zugang_fachstelle_item = models.CharField(max_length=100, null=True,  blank=True) # (Flyer, Internet, ...)

# Betroffene Person
class Person(models.Model): 
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    alter_item = models.CharField(max_length=100) # String weil Kohorten
    anzahl_kinder = models.IntegerField(null=True, blank=True)
    gender_item = models.CharField(max_length=100)
    vorgang = models.OneToOneField(Vorgang, on_delete=models.CASCADE, null=True, blank=True)
    betroffen_item = models.CharField(max_length=100, null=True, blank=True) # (Alleinstehend, Familie, usw.)
    prozeskostenuebernahme_item = models.CharField(max_length=100, null=True, blank=True) # (Ja, Nein, zu prüfen, anderes)

# Verursacher
class Verursacher(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    unternehmenstyp_item = models.CharField(max_length=100) # (städtisch, land, privat usw.)
    personentyp_item = models.CharField(max_length=100) # (Hausmeister, Hausverwaltung)
    vorgang = models.ForeignKey(Vorgang, on_delete=models.CASCADE)

class Intervention(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    vorgang_id = models.ForeignKey(Vorgang, on_delete=models.CASCADE)
    datum = models.DateField()
    form_item = models.CharField(max_length=100)
    bemerkung = models.TextField()


class Item(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    key = models.CharField(max_length=100)  # TODO: bessere Datentyp?
    value = models.CharField(max_length=100)


class FormTextMixin(models.Model):
    class Meta:
        abstract = True
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model = models.CharField(max_length=100, choices=[], default=None)
    field = models.CharField(max_length=100, default=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('model').choices = self.get_model_choices()

    @staticmethod
    def get_model_choices():
        models_list = apps.get_models()
        return [(model.__name__, model.__name__) for model in models_list]


class FormValues(FormTextMixin):
    value = models.CharField(max_length=100)

class FormLabels(FormTextMixin):
    label = models.CharField(max_length=100)

    @staticmethod
    def get_Label(modelname, fieldname):
        object = FormLabels.objects.get(model=modelname, field=fieldname)
        if(object):
            return object.label
        else:
            return fieldname
        