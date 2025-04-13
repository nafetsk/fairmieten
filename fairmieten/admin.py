import unfold
from django.contrib import admin
from .models import (
    Diskrimminierungsart,
    Diskriminierung,
    FormValues,
    FormLabels,
    Loesungsansaetze,
    Ergebnis,
    Rechtsbereich,
    Vorgang,
    Intervention,
    Verursacher,
    Diskriminierungsform,
)
from aggregation.models import Charts

class FormLabelsAdmin(unfold.admin.ModelAdmin):
    list_display = ('model', 'field', 'label')
    search_fields = ('model', 'field', 'label')  # Ermöglicht die Suche nach 'field' und 'label'
    ordering = ('model', 'field')

class FormValuesAdmin(unfold.admin.ModelAdmin):
    list_display = ('model', 'field', 'key', 'value', 'encoding')
    search_fields = ('model', 'field', 'value')  # Ermöglicht die Suche nach 'field' und 'label'
    ordering = ('model', 'field')

# Register your models here.
admin.site.register(Diskrimminierungsart, unfold.admin.ModelAdmin)
admin.site.register(Diskriminierung, unfold.admin.ModelAdmin)
admin.site.register(Loesungsansaetze, unfold.admin.ModelAdmin)
admin.site.register(Ergebnis, unfold.admin.ModelAdmin)
admin.site.register(FormValues, FormValuesAdmin)
admin.site.register(FormLabels,FormLabelsAdmin)
admin.site.register(Charts, unfold.admin.ModelAdmin)
admin.site.register(Diskriminierungsform, unfold.admin.ModelAdmin)
admin.site.register(Vorgang)
admin.site.register(Rechtsbereich)
admin.site.register(Verursacher)
#admin.site.register(Intervention)


