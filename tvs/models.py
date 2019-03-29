from django.db import models
from django.utils.datetime_safe import datetime

class Tv(models.Model):
    idTv = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=40)
    status = models.DateTimeField(default=datetime.now(), blank=True)

    def __str__(self):
        return self.nome
