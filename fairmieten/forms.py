from django import forms
from .models import Vorgang

class VorgangForm(forms.ModelForm):
    class Meta:
        model = Vorgang
        fields = [
            'datum_kontakaufnahme',
            'datum_vorfall_von',
            'datum_vorfall_bis',
            'sprache',
            'beschreibung',
            'bezirk_item',
            'diskriminierung',
            'loesungsansaetze',
            'ergebnis'
        ]
        widgets = {
            'datum_kontakaufnahme': forms.DateInput(attrs={'type': 'date'}),
            'datum_vorfall_von': forms.DateInput(attrs={'type': 'date'}),
            'datum_vorfall_bis': forms.DateInput(attrs={'type': 'date'}),
        }
