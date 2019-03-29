from django.db import models
from tvs.models import Tv
from produtos.models import Produto
from ofertas.models import Oferta

class Tela(models.Model):

    lista_tipo = (
        ("","Selecione"),
        ("oferta","Oferta"),
        ("tabela","Tabela"),
        ("video","Video"),
    )

    idTela = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=45)
    tempoexibicao = models.CharField(max_length=45)
    video = models.FileField(upload_to='videos/', null=True, verbose_name="")
    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE, null=True)
    tipo = models.CharField(max_length=10, choices=lista_tipo)
    tv = models.ForeignKey(Tv, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class IntensTela(models.Model):
    idIntensTela = models.AutoField(primary_key=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tela = models.ForeignKey(Tela, on_delete=models.CASCADE)
    ordem = models.CharField(max_length=10)

    def __str__(self):
        return self.tela.nome
