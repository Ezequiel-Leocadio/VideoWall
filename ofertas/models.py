

from django.db import models
from django.utils import timezone
from django.utils.datetime_safe import datetime

from produtos.models import Produto

class Oferta(models.Model):
    idOferta = models.AutoField(primary_key=True)
    codigo = models.IntegerField()
    nome = models.CharField(max_length=40)
    datainicio = models.DateTimeField(default=datetime.now(), blank=True)
    datafim = models.DateTimeField(default=datetime.now(), blank=True)



    def __str__(self):
        return self.nome

class IntensOferta(models.Model):
    idIntensOferta = models.AutoField(primary_key=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE)
    ordem = models.CharField(max_length=10)


    def __str__(self):
        return self.produto.descricaoexibicao

