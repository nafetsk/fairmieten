from django.db import models

class Vorgang(models.Model):
    vorgang_id = models.AutoField(primary_key=True)
    datum_der_kontakaufnahme = models.DateField()
    sprache = models.CharField(max_length=100)
    

class 