from django.contrib import admin
from .models import Diskrimminierungsart, Diskriminierung, Loesungsansaetze, Ergebnis, Vorgang, Intervention, Item


# Register your models here.
admin.site.register(Diskrimminierungsart)
admin.site.register(Diskriminierung)
admin.site.register(Loesungsansaetze)
admin.site.register(Ergebnis)
admin.site.register(Vorgang)
admin.site.register(Intervention)
admin.site.register(Item)