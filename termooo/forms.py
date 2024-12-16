from django import forms
from .models import Palavra

class PalavraForm(forms.ModelForm):
    class Meta:
        model = Palavra
        fields = ['texto']

