import datetime
import uuid
from django.apps import apps
from django.db import models
from django.contrib.auth.models import User


class Vorgangstyp(models.Model):
    id = models.IntegerField( primary_key = True, editable = False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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
    
class Diskriminierungsform(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    name = models.CharField(max_length=100)

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
    # Allgemein
    fallnummer = models.CharField(max_length=100, null=True, blank=True)
    vorgangstyp = models.ForeignKey(Vorgangstyp, on_delete=models.CASCADE, null=True, blank=True) # allgemeine Beratung, Meldung, Fallbetreuung
    datum_kontaktaufnahme = models.DateField(null=True, blank=True, default=datetime.date.today)
    kontaktaufnahme_durch_item = models.CharField(max_length=100, null=True, blank=True) # (Betroffene Person, beschuldigte Person, unbeteiligte Person)
    datum_vorfall_von = models.DateField(null=True, blank=True)
    datum_vorfall_bis = models.DateField(null=True, blank=True)
    sprache_item = models.CharField(max_length=100, null=True, blank=True)
    andere_sprache = models.CharField(max_length=100, null=True, blank=True)
    beschreibung = models.TextField(null=True, blank=True)
    bezirk_item = models.CharField(max_length=100, null=True, blank=True)
    zugang_fachstelle_item = models.CharField(max_length=100, null=True,  blank=True) # (Flyer, Internet, ...)

    # Betroffene Person
    alter_item = models.CharField(max_length=100, null=True, blank=True) # String weil Kohorten
    anzahl_kinder = models.IntegerField(null=True, blank=True)
    gender_item = models.CharField(max_length=100, null=True, blank=True)
    betroffen_item = models.CharField(max_length=100, null=True, blank=True) # (Alleinstehend, Familie, usw.)
    prozeskostenuebernahme_item = models.CharField(max_length=100, null=True, blank=True) # (Ja, Nein, zu prüfen, anderes)
    bereich_diskriminierung_item = models.CharField(max_length=100, null=True, blank=True) # (Wohnungssuche, Gewerbe)
    anderer_bereich_diskriminierung = models.CharField(max_length=100, null=True, blank=True)
    diskriminierungsform = models.ManyToManyField(Diskriminierungsform, blank=True) # (Unmittelbar, mittelbar, usw.)
    andere_diskriminierungsform = models.CharField(max_length=100, null=True, blank=True)

    # Diskriminierung
    diskriminierung = models.ManyToManyField(Diskriminierung, blank=True)
    andere_diskriminierung = models.CharField(max_length=100, null=True, blank=True)
    # Loesungsansaetze
    loesungsansaetze = models.ManyToManyField(Loesungsansaetze, blank=True)
    rechtsbereich = models.ManyToManyField(Rechtsbereich, blank=True)
    loesungsansaetze_bemerkung = models.TextField(null=True, blank=True)
    # Ergebnis
    ergebnis = models.ManyToManyField(Ergebnis, blank=True)
    ergebnis_bemerkung = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.fallnummer)
    


# Verursacher
class Verursacher(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False)
    unternehmenstyp_item = models.CharField(max_length=100) # (städtisch, land, privat usw.)
    personentyp_item = models.CharField(max_length=100) # (Hausmeister, Hausverwaltung)
    vorgang = models.ForeignKey(Vorgang, on_delete=models.CASCADE)

class Intervention(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False)
    vorgang = models.ForeignKey(Vorgang, on_delete=models.CASCADE)
    datum = models.DateField(null=True, blank=True)
    form_item = models.CharField(max_length=100, null=True, blank=True)
    bemerkung = models.TextField(null=True, blank=True)


class Item(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False)
    key = models.CharField(max_length=100) 
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
    key = models.CharField(max_length=100, default=None, null=True, blank=True)
    value = models.CharField(max_length=100)
    # Encoding für csv-Export
    encoding = models.IntegerField(default=0)

    @staticmethod
    def get_Values(modelname, empty_value=None):
        values = FormValues.objects.filter(model=modelname)
        values_dict = {}
        for value in values:
            if value.field not in values_dict:
                values_dict[value.field] = [('', empty_value)] if empty_value else []
            values_dict[value.field].append((value.key, value.value))
        return values_dict

    @staticmethod
    def get_field_values(field_name):
        values = FormValues.objects.filter(field=field_name)
        if not values:
            return None
        choices = []
        for value in values:
            choices.append((value.key, value.value))
        return choices
    

class FormLabels(FormTextMixin):
    label = models.CharField(max_length=100)
