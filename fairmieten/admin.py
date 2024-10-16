import unfold
from django.contrib import admin
from .models import (
    Diskrimminierungsart,
    Diskriminierung,
    FormValues,
    FormLabels,
    Loesungsansaetze,
    Ergebnis,
    Vorgang,
    Intervention,
    Person,
    Verursacher,
)
from aggregation.models import Charts

class FormLabelsAdmin(unfold.admin.ModelAdmin):
    list_display = ('model', 'field', 'label')
    search_fields = ('model', 'field', 'label')  # Ermöglicht die Suche nach 'field' und 'label'
    ordering = ('model', 'field')

class FormValuesAdmin(admin.ModelAdmin):
    list_display = ('model', 'field', 'key', 'value')
    search_fields = ('model', 'field', 'value')  # Ermöglicht die Suche nach 'field' und 'label'
    ordering = ('model', 'field')

# Register your models here.
admin.site.register(Diskrimminierungsart, unfold.admin.ModelAdmin)
admin.site.register(Diskriminierung, unfold.admin.ModelAdmin)
admin.site.register(Loesungsansaetze)
admin.site.register(Ergebnis)
admin.site.register(Vorgang)
admin.site.register(Intervention)
admin.site.register(FormValues, FormValuesAdmin)
admin.site.register(FormLabels,FormLabelsAdmin)
admin.site.register(Charts)
admin.site.register(Person)
admin.site.register(Verursacher)


