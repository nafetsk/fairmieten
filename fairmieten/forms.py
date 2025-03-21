from django import forms
from .models import (
    Diskriminierung,
    FormLabels,
    FormValues,
    Intervention,
    Verursacher,
    Vorgang,
    Loesungsansaetze,
    Rechtsbereich,
    Ergebnis,
    Diskriminierungsform,
)
from .widgets import CustomCheckboxMultiSelectInput


class DataTextForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #print(self.Meta.model.__name__)
        labels = dict(
            FormLabels.objects.filter(model=self.Meta.model.__name__).values_list(
                "field", "label"
            )
        )
        values_dict = FormValues.get_Values(self.Meta.model.__name__, empty_value=' ')

        for field_name in self.fields:
            if field_name.endswith("_item") and field_name in values_dict:
                self.fields[field_name] = forms.ChoiceField(
                    choices=values_dict[field_name], required=False
                )
            
            #print(field_name)
            self.fields[field_name].label = labels.get(field_name, field_name)
    
    # def save(self, commit=True):
    #     if self.errors:
    #         raise ValueError(
    #             "The %s could not be %s because the data didn't validate."
    #             % (
    #                 self.instance._meta.object_name,
    #                 "created" if self.instance._state.adding else "changed",
    #             )
    #         )
    #     if commit:
    #         self.instance.save(update_fields=self.changed_data)
    #         self._save_m2m()
    #     else:
    #         self.save_m2m = self._save_m2m
    #     return self.instance


class BeratungForm(DataTextForm):
    class Meta:
        model = Vorgang
        fields = [
            "fallnummer",
            "kontaktaufnahme_durch_item",
            "datum_kontaktaufnahme",
            "beschreibung",
            "zugang_fachstelle_item",
        ]
        widgets = {
            "datum_kontaktaufnahme": forms.DateInput(attrs={"type": "date"}),
        }


class VorgangForm(DataTextForm):

    class Meta:
        model = Vorgang
        fields = [
            "fallnummer",
            "kontaktaufnahme_durch_item",
            "datum_kontaktaufnahme",
            "datum_vorfall_von",
            "datum_vorfall_bis",
            "sprache_item",
            "andere_sprache",
            "beschreibung",
            "bezirk_item",
            "zugang_fachstelle_item",
        ]
        widgets = {
            "datum_kontaktaufnahme": forms.DateInput(attrs={"type": "date"}),
            "datum_vorfall_von": forms.DateInput(attrs={"type": "date"}),
            "datum_vorfall_bis": forms.DateInput(attrs={"type": "date"}),
        }



class PersonForm(DataTextForm):
    class Meta:
        model = Vorgang
        fields = [
            "alter_item",
            "anzahl_kinder",
            "gender_item",
            "betroffen_item",
            "prozeskostenuebernahme_item",
            "bereich_diskriminierung_item",
            "anderer_bereich_diskriminierung",
            "diskriminierungsform",
            "andere_diskriminierungsform",
        ]
        widgets = {"anzahl_kinder": forms.NumberInput(attrs={"min": 0})}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields["diskriminierungsform"].widget = CustomCheckboxMultiSelectInput()
        self.fields["diskriminierungsform"].queryset = Diskriminierungsform.objects.all()


class DiskriminierungForm(DataTextForm):
    class Meta:
        model = Vorgang
        fields = ["diskriminierung", "andere_diskriminierung"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Custom HTML für die Buttons der Checkboxen
        self.fields["diskriminierung"].widget = CustomCheckboxMultiSelectInput()
        self.fields[
            "diskriminierung"
        ].queryset = Diskriminierung.objects.select_related("typ").all()
        self.diskriminierung_instances = list(self.fields["diskriminierung"].queryset)


class LoesungsansaetzeForm(DataTextForm):
    class Meta:
        model = Vorgang
        fields = [
            "loesungsansaetze",
            "rechtsbereich",
            "loesungsansaetze_bemerkung",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Custom HTML für die Buttons der Checkboxen
        self.fields["loesungsansaetze"].widget = CustomCheckboxMultiSelectInput()
        self.fields["loesungsansaetze"].queryset = Loesungsansaetze.objects.all()
        self.fields["rechtsbereich"].widget = CustomCheckboxMultiSelectInput()
        self.fields["rechtsbereich"].queryset = Rechtsbereich.objects.all()


class ErgebnisForm(DataTextForm):
    class Meta:
        model = Vorgang
        fields = ["ergebnis", "ergebnis_bemerkung"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Custom HTML für die Buttons der Checkboxen
        self.fields["ergebnis"].widget = CustomCheckboxMultiSelectInput()
        self.fields["ergebnis"].queryset = Ergebnis.objects.all()

# Form für Verursacher
class VerursacherForm(DataTextForm):
    class Meta:
        model = Verursacher
        fields = ['unternehmenstyp_item', 'personentyp_item']


# Form für Intervention
class InterventionForm(DataTextForm):
    class Meta:
        model = Intervention
        fields = ['datum', 'form_item', 'bemerkung']
        widgets = {
            "datum": forms.DateInput(attrs={"type": "date"}),
            "bemerkung": forms.Textarea(attrs={"rows": 2, "placeholder": "Bemerkung"}),
        }
