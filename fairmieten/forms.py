from django import forms
from .models import Vorgang, Person

class VorgangForm(forms.ModelForm):
    class Meta:
        model = Vorgang
        fields = [
            "fallnummer",
            "kontakaufnahme_durch_item",
            'datum_kontakaufnahme',
            'datum_vorfall_von',
            'datum_vorfall_bis',
            'sprache',
            'beschreibung',
            'bezirk_item',
        ]
        widgets = {
            'datum_kontakaufnahme': forms.DateInput(attrs={'type': 'date'}),
            'datum_vorfall_von': forms.DateInput(attrs={'type': 'date'}),
            'datum_vorfall_bis': forms.DateInput(attrs={'type': 'date'}),
        }

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'alter_item',
            'anzahl_kinder',
            'gender_item',
        ]
        widgets = {
            'alter_item': forms.Select(choices=[
                ('0-18', '0-18 Jahre'),
                ('19-30', '19-30 Jahre'),
                ('31-50', '31-50 Jahre'),
                ('51-65', '51-65 Jahre'),
                ('65+', '65+ Jahre'),
            ]),
            'anzahl_kinder': forms.NumberInput(attrs={'min': 0}),
            'gender_item': forms.Select(choices=[
                ('maennlich', 'Männlich'),
                ('weiblich', 'Weiblich'),
                ('divers', 'Divers'),
                ('keine_angabe', 'Keine Angabe'),
            ]),
        }

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.fields['anzahl_kinder'].required = False
        self.fields['alter_item'].label = "Altersgruppe"
        self.fields['anzahl_kinder'].label = "Anzahl der Kinder"
        self.fields['gender_item'].label = "Geschlecht"
