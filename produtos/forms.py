from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Produto

class ProdutoForm(forms.ModelForm):
    valor = forms.DecimalField(max_digits=8, decimal_places=2, localize=True)
    class Meta:
        model = Produto
        fields = ["codigo","valor", "tipoproduto","descricaoexibicao", "imagem"]


class ProdutoImagemForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ["imagem"]