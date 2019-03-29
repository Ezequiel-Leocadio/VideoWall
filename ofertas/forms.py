from django import forms



class ItemOfertaForm(forms.Form):
    produto_id = forms.CharField(label='ID do Produto', max_length=100)

