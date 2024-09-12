from django import forms

from .models import Hello

class HelloForm(forms.ModelForm):

    class Meta:
         model = Hello
         fields = ('content',)
