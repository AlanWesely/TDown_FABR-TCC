from django.db import models


# Create your models here.
class Modalidade(models.Model):
    tipoModalidade = models.CharField(max_length=100)


class Time(models.Model):
    nomeEquipe = models.CharField(max_length=100)
    nomeAbreviado = models.CharField(max_length=50)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    modalidadeMasc = models.BooleanField(default=False)
    modalidadeFem = models.BooleanField(default=False)
    logoTime = models.ImageField('app_tdown/logoTime/')


class Liga(models.Model):
    nomeLiga = models.CharField(max_length=100)
    federacao = models.CharField(max_length=100)
    serieDivisao = models.CharField(max_length=300)


class Partida(models.Model):
    timeCasa = models.ForeignKey(
        Time, on_delete=models.SET_NULL, null=True
        )
    timeVisitante = models.ForeignKey(
        Time, on_delete=models.SET_NULL, null=True
        )
    dataPartida = models.DateField()
    horarioPartida = models.TimeField()
    ruaPartida = models.CharField(max_length=200)
    numeroPartida = models.CharField(max_length=10)
    cidadePartida = models.CharField(max_length=150)
    estadoPartida = models.CharField(max_length=2)
    ligaPartida = models.ForeignKey(
        Liga, on_delete=models.SET_NULL, null=True
    )
    modalidadePartida = models.ForeignKey(
        Modalidade, on_delete=models.SET_NULL, null=True
    )

