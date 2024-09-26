from django import forms
from .models import Vorgang

class VorgangForm(forms.ModelForm):
    class Meta:
        model = Vorgang
        fields = [
            'datum_kontakaufnahme',
            'datum_vorfall_von',
            'uhrzeit_vorfall',
            'datum_vorfall_bis',
            'sprache',
            'beschreibung',
            'plz',
            'bezirk_item',
            'diskriminierung',
            'loesungsansaetze',
            'ergebnis'
        ]
        widgets = {
            'datum_kontakaufnahme': forms.DateInput(attrs={'type': 'date'}),
            'datum_vorfall_von': forms.DateInput(attrs={'type': 'date'}),
            'datum_vorfall_bis': forms.DateInput(attrs={'type': 'date'}),
            'uhrzeit_vorfall': forms.TimeInput(attrs={'type': 'time'}),
        }
