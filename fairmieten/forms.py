import logging
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

        labels = dict(
            FormLabels.objects.filter(model=self.Meta.model.__name__).values_list(
                "field", "label"
            )
        )
        values_dict = FormValues.get_Values(self.Meta.model.__name__)

        for field_name in self.fields:
            if field_name.endswith("_item") and field_name in values_dict:
                self.fields[field_name] = forms.ChoiceField(
                    choices=values_dict[field_name], required=False
                )
            if field_name == "loesungsansaetze_bemerkung":
                print("dict_result:" + labels.get(field_name, field_name))
            self.fields[field_name].label = labels.get(field_name, field_name)

        # Überprüfe, ob das Feld einen Wert aus der Datenbank hat
        for field_name in self.fields:
            if (self.instance and self.instance.pk is not None ):  # Überprüfen, ob das Objekt existiert
                field_value = getattr(self.instance, field_name, None)
                if (
                    field_value is not None and field_value != ""
                ):  # Überprüfen, ob das Feld einen Wert hat
                    # Füge die Klasse "from_database" hinzu
                    current_class = self.fields[field_name].widget.attrs.get(
                        "class", ""
                    )
                    self.fields[field_name].widget.attrs["class"] = " ".join(
                        filter(None, [current_class, "from_database"])
                    )


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
            "bereich_diskriminierung_item",
            "diskriminierungsform",
        ]
        widgets = {"anzahl_kinder": forms.NumberInput(attrs={"min": 0})}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields["diskriminierungsform"].widget = CustomCheckboxMultiSelectInput()
        self.fields["diskriminierungsform"].queryset = Diskriminierungsform.objects.all()


class DiskriminierungForm(forms.ModelForm):
    class Meta:
        model = Vorgang
        fields = ["diskriminierung"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Custom HTML für die Buttons der Checkboxen
        self.fields["diskriminierung"].widget = CustomCheckboxMultiSelectInput()
        self.fields[
            "diskriminierung"
        ].queryset = Diskriminierung.objects.select_related("typ").all()
        self.diskriminierung_instances = list(self.fields["diskriminierung"].queryset)


class LoesungsansaetzeForm(forms.ModelForm):
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


class ErgebnisForm(forms.ModelForm):
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

