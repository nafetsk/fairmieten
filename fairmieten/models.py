from django.db import models


class Diskrimminierungsart(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Diskriminierung(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    typ = models.ForeignKey(Diskrimminierungsart, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Loesungsansaetze(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class Ergebnis(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

# Betroffene Person
class Person(models.Model): 
    id = models.AutoField(primary_key=True)
    alter_item = models.CharField(max_length=100) # String weil Kohorten
    anzahl_kinder = models.IntegerField(null=True, blank=True)
    gender_item = models.CharField(max_length=100)

class Vorgang(models.Model):
    id = models.AutoField(primary_key=True)
    fallnummer = models.IntegerField(null=True, blank=True)
    datum_kontakaufnahme = models.DateField(null=True, blank=True)
    datum_vorfall_von = models.DateField(null=True, blank=True)
    datum_vorfall_bis = models.DateField(null=True, blank=True)
    sprache = models.CharField(max_length=100)
    beschreibung = models.TextField(null=True, blank=True)
    bezirk_item = models.CharField(max_length=100)
    diskriminierung = models.ManyToManyField(Diskriminierung, blank=True)
    loesungsansaetze = models.ManyToManyField(Loesungsansaetze, blank=True)
    ergebnis = models.ManyToManyField(Ergebnis, blank=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)

# Verursacher
class Verursacher(models.Model):
    id = models.AutoField(primary_key=True)
    unternehmenstyp_item = models.CharField(max_length=100) # (städtisch, land, privat usw.)
    personentyp_item = models.CharField(max_length=100) # (Hausmeister, Hausverwaltung)
    vorgang = models.ForeignKey(Vorgang, on_delete=models.CASCADE)

class Intervention(models.Model):
    id = models.AutoField(primary_key=True)
    vorgang_id = models.ForeignKey(Vorgang, on_delete=models.CASCADE)
    datum = models.DateField()
    form_item = models.CharField(max_length=100)
    bemerkung = models.TextField()


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=100)  # TODO: bessere Datentyp?
    value = models.CharField(max_length=100)


class Charts(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)

    def __str__(self):
        return self.name
