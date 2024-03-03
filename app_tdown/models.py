from django.db import models


# Create your models here.
class Modalidade(models.Model):
    tipoModalidade = models.CharField(max_length=100)

    def __str__(self):
        return self.tipoModalidade
    

class Federacoes(models.Model):
    nomeAbrev = models.CharField(max_length=10)
    nomeFederacao = models.CharField(max_length=100)

    def __str__(self):
        return self.nomeAbrev


class Time(models.Model):
    nomeEquipe = models.CharField(max_length=100)
    nomeAbreviado = models.CharField(max_length=50)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    modalidadeMasc = models.BooleanField(default=False)
    modalidadeFem = models.BooleanField(default=False)
    logoTime = models.ImageField(upload_to='app_tdown/covers/logoTime/')
    
    def __str__(self):
        return self.nomeAbreviado


class Liga(models.Model):
    nomeAbrevLiga = models.CharField(max_length=10)
    nomeLiga = models.CharField(max_length=100)
    federacao = models.ForeignKey(
        Federacoes, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.nomeAbrevLiga

class DivisoesCampeonatos(models.Model):
    nomeEDivisao = models.CharField(max_length=100)
    liga = models.ForeignKey(
        Liga, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.nomeEDivisao


class Partida(models.Model):
    nomePartida = models.CharField(max_length=300)
    timeCasa = models.ForeignKey(
        Time, related_name='partidas_casa', on_delete=models.SET_NULL, null=True
        )
    timeVisitante = models.ForeignKey(
        Time, related_name='partidas_visitante', on_delete=models.SET_NULL, null=True
        )
    dataPartida = models.DateField()
    horarioPartida = models.TimeField()
    ruaPartida = models.CharField(max_length=200)
    numeroPartida = models.CharField(max_length=10)
    cidadePartida = models.CharField(max_length=150)
    estadoPartida = models.CharField(max_length=2)
    divisoePartida = models.ForeignKey(
        DivisoesCampeonatos, on_delete=models.SET_NULL, null=True
    )
    ligaPartida = models.ForeignKey(
        Liga, on_delete=models.SET_NULL, null=True
    )
    modalidadePartida = models.ForeignKey(
        Modalidade, on_delete=models.SET_NULL, null=True
    )
    logoPartida = models.ImageField(upload_to='app_tdown/covers/logoPartida/', blank=True, default='')



    def __str__(self):
        return self.nomePartida