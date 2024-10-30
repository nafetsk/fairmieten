from django import forms
from .models import (
    Diskriminierung,
    FormLabels,
    FormValues,
    Vorgang,
    Person,
    Loesungsansaetze,
    Rechtsbereich,
    Ergebnis,
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
            self.fields[field_name].label = labels.get(field_name, field_name)

        # Überprüfe, ob das Feld einen Wert aus der Datenbank hat
        for field_name in self.fields:
            if (
                self.instance and self.instance.pk is not None
            ):  # Überprüfen, ob das Objekt existiert
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


class VorgangForm(DataTextForm):
    class Meta:
        model = Vorgang
        fields = [
            "fallnummer",
            "kontaktaufnahme_durch_item",
            "datum_kontaktaufnahme",
            "datum_vorfall_von",
            "datum_vorfall_bis",
            "sprache",
            "beschreibung",
            "bezirk_item",
        ]
        widgets = {
            "datum_kontaktaufnahme": forms.DateInput(attrs={"type": "date"}),
            "datum_vorfall_von": forms.DateInput(attrs={"type": "date"}),
            "datum_vorfall_bis": forms.DateInput(attrs={"type": "date"}),
        }


class PersonForm(DataTextForm):
    class Meta:
        model = Person
        fields = [
            "alter_item",
            "anzahl_kinder",
            "gender_item",
        ]
        widgets = {"anzahl_kinder": forms.NumberInput(attrs={"min": 0})}


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
