import uuid
from django.db import models


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
    sprache = models.CharField(max_length=100)
    beschreibung = models.TextField(null=True, blank=True)
    bezirk_item = models.CharField(max_length=100)
    diskriminierung = models.ManyToManyField(Diskriminierung, blank=True)
    loesungsansaetze = models.ManyToManyField(Loesungsansaetze, blank=True)
    ergebnis = models.ManyToManyField(Ergebnis, blank=True)

# Betroffene Person
class Person(models.Model): 
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    alter_item = models.CharField(max_length=100) # String weil Kohorten
    anzahl_kinder = models.IntegerField(null=True, blank=True)
    gender_item = models.CharField(max_length=100)
    vorgang = models.ForeignKey(Vorgang, on_delete=models.CASCADE, null=True, blank=True)


# TODO: es fehlt noch "Wer ist Betroffen", 
# Träger Institution?, 
# Prozesskostenübernahme?,
# Relevante Rechtsbeieiche

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


class Charts(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False)
    type = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    variable = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
