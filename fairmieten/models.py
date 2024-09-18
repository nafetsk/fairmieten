from django.db import models

class Diskrimminierungsart(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
    
class Diskriminierung(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    typ = models.ForeignKey(Diskrimminierungsart, on_delete=models.CASCADE)

class Loesungsansaetze(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class Ergebnis(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class Vorgang(models.Model):
    id = models.AutoField(primary_key=True)
    datum_kontakaufnahme = models.DateField()
    datum_vorfall_von = models.DateField()
    uhrzeit_vorfall = models.TimeField(null=True, blank=True)
    datum_vorfall_bis = models.DateField(null=True, blank=True)
    sprache = models.CharField(max_length=100)
    beschreibung = models.TextField()
    plz = models.IntegerField()
    bezirk_item = models.CharField(max_length=100)
    diskriminierung = models.ManyToManyField(Diskriminierung, blank=True)
    diskriminierungsart = models.ManyToManyField(Diskrimminierungsart, blank=True)
    loesungsansaetze = models.ManyToManyField(Loesungsansaetze, blank=True)
    ergebnis = models.ManyToManyField(Ergebnis, blank=True)

class Intervention(models.Model):
    id = models.AutoField(primary_key=True)
    vorgang_id = models.ForeignKey(Vorgang, on_delete=models.CASCADE)
    datum = models.DateField()
    form_item = models.CharField(max_length=100)
    bemerkung = models.TextField()  
    
class Item(models.Model):
	id = models.AutoField(primary_key=True)
	key = models.CharField(max_length=100) #TODO: bessere Datentyp? 
	value = models.CharField(max_length=100)
 
 #TODO: Beweise anlegen
 
 #TODO: Personendaten ?
    
    

