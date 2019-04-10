from django.db import models

class Tvs(models.Model):
    idTv = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=40)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    idProduto = models.AutoField(primary_key=True)
    codigo = models.IntegerField()
    descricaoimportcao = models.CharField(max_length=50)
    descricaoexibicao = models.CharField(max_length=80)
    valor = models.DecimalField(max_digits=11, decimal_places=2)
    tipoproduto = models.IntegerField()
    imagem = models.ImageField(upload_to='produtos', null=True, blank=True)




    def __str__(self):
        return str(self.codigo)+str(' -- '+self.descricaoexibicao)