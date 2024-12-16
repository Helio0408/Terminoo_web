from django import forms
from .models import Palavra

class PalavraForm(forms.ModelForm):
    class Meta:
        model = Palavra
        fields = ['texto']

    def clean_texto(self):
        texto = self.cleaned_data.get('texto')

        if len(texto) != 5:
            raise forms.ValidationError("A palavra deve ter exatamente 5 letras.")

        return texto


