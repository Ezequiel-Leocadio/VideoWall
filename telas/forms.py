from django import forms
from .models import Tela

class TelaForm(forms.ModelForm):
    class Meta:
        model = Tela
        fields = ["nome", "tempoexibicao", "tipo", "video"]


class ItemTelaForm(forms.ModelForm):
    produto_id = forms.CharField(label='ID do Produto', max_length=100)

class TelaVideoForm(forms.ModelForm):
    class Meta:
        model = Tela
        fields = [ "video"]