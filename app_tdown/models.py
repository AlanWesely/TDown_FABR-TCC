from django.db import models


# Create your models here.
#####################################################################################################################
#SEGUE BASE MODEL DA TABELA MODALIDADE
######################################################################################################################
class Modalidade(models.Model):
    tipoModalidade = models.CharField(max_length=100)

    def __str__(self):
        return self.tipoModalidade
    
#####################################################################################################################
#SEGUE BASE MODEL DA TABELA FEDERAÇÃO
######################################################################################################################
class Federacoes(models.Model):
    nomeAbrev = models.CharField(max_length=10)
    nomeFederacao = models.CharField(max_length=100)

    def __str__(self):
        return self.nomeAbrev

#####################################################################################################################
#SEGUE BASE MODEL DA TABELA TIME
######################################################################################################################
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

#####################################################################################################################
#SEGUE BASE MODEL DA TABELA LIGA
######################################################################################################################
class Liga(models.Model):
    nomeAbrevLiga = models.CharField(max_length=10)
    nomeLiga = models.CharField(max_length=100)
    federacao = models.ForeignKey(
        Federacoes, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.nomeAbrevLiga

#####################################################################################################################
#SEGUE BASE MODEL DA TABELA DIVISÕES CAMPEONATO
######################################################################################################################
class DivisoesCampeonatos(models.Model):
    nomeEDivisao = models.CharField(max_length=100)
    liga = models.ForeignKey(
        Liga, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.nomeEDivisao

#####################################################################################################################
#SEGUE BASE MODEL DA TABELA PARTIDA
######################################################################################################################
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
    
#########################################################################################################################
#SEGUE BASE MODEL DA TABELA JOGADA
#########################################################################################################################
class Jogada(models.Model):
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    jogada = models.IntegerField()
    tempo = models.IntegerField()
    descida = models.IntegerField()
    timeAtacando = models.ForeignKey(Time, on_delete=models.SET_NULL, null=True, related_name='time_atacando')
    timeDefendendo = models.ForeignKey(Time, on_delete=models.SET_NULL, null=True, related_name='time_defendendo')
    jardaFirst = models.IntegerField()
    posicaoBola = models.IntegerField()

    def __str__(self):
        return f"Jogada {self.jogada} - Tempo {self.tempo}"

####################################################################################################################################
# SEGUE BASE MODEL DA TABELA FALTA
####################################################################################################################################
class Falta(models.Model):
    nomeFalta = models.CharField(max_length=250)
    penalidade = models.CharField(max_length=500)
    descFalta = models.CharField(max_length=800)

    def __str__(self):
        return self.nomeFalta

#########################################################################################################################
#SEGUE BASE MODEL DA TABELA FALTA COMETIDA
#########################################################################################################################
class FaltaCometida(models.Model):
    conclusaoJogada = models.ForeignKey("ConclusaoJogada", on_delete=models.CASCADE)
    tipoFalta = models.ForeignKey(Falta, on_delete=models.CASCADE)
    timeCometeuFalta = models.ForeignKey(Time, on_delete=models.CASCADE)
    num_jogadorFezFalta = models.IntegerField()

    def __str__(self):
        return f"{self.tipoFalta} cometida pelo jogador {self.num_jogadorFezFalta}"

#########################################################################################################################
#SEGUE BASE MODEL DA TABELA PONTUACAO
#########################################################################################################################
class Pontuacao(models.Model):
    nomePontuacao = models.CharField(max_length=25)
    descPontuacao = models.CharField(max_length=2000)
    qtsPonto = models.IntegerField()

    def __str__(self):
        return self.nomePontuacao

#########################################################################################################################
#SEGUE BASE MODEL DA TABELA CONCLUSAO JOGADA
#########################################################################################################################
class ConclusaoJogada(models.Model):
    jogada = models.ForeignKey(Jogada, on_delete=models.CASCADE)
    tipoJogada = models.CharField(max_length=25)
    possuiFalta = models.BooleanField(default=False)
    jogPossuiFumble = models.BooleanField(default=False)
    timeAtaqueRecuperou = models.BooleanField(default=False)
    jogadaComPontuacao = models.BooleanField(default=False)
    tipoPontuacao = models.ForeignKey(Pontuacao, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Conclusão da Jogada {self.jogada.id}"

#########################################################################################################################
#SEGUE BASE MODEL DA TABELA PASSE
#########################################################################################################################
class Passe(models.Model):
    conclusaoJogada = models.ForeignKey(ConclusaoJogada, on_delete=models.CASCADE)
    n_quaterback = models.IntegerField()
    n_recebedor = models.IntegerField()
    resultado_jogada = models.CharField(max_length=50)
    direcao_passe = models.CharField(max_length=50)
    qt_jard_percorreu = models.IntegerField()
    profundidade_passe = models.CharField(max_length=50)
    def_parou_jogada = models.BooleanField(default=False)
    jogador_parou_jogada = models.IntegerField()

    def __str__(self):
        return f"Passe do QB {self.n_quaterback}"

#########################################################################################################################
#SEGUE BASE MODEL DA TABELA CORRIDA
#########################################################################################################################
class Corrida(models.Model):
    conclusaoJogada = models.ForeignKey(ConclusaoJogada, on_delete=models.CASCADE)
    n_quaterback = models.IntegerField()
    n_corredor = models.IntegerField()
    resultado_jogada = models.CharField(max_length=50)
    direcao_corrida = models.CharField(max_length=50)
    qt_jard_percorreu = models.IntegerField()
    gap_corrida = models.CharField(max_length=10)
    def_parou_jogada = models.BooleanField(default=False)
    jogador_parou_jogada = models.IntegerField()

    def __str__(self):
        return f"Corrida do jogador {self.n_corredor}"

#########################################################################################################################
#SEGUE BASE MODEL DA TABELA PUNT
#########################################################################################################################
class Punt(models.Model):
    conclusaoJogada = models.ForeignKey(ConclusaoJogada, on_delete=models.CASCADE)
    n_kicker = models.IntegerField()
    resultado_jogada = models.CharField(max_length=50)
    posicao_campo = models.IntegerField()
    qt_jard_punt = models.IntegerField()
    teve_retorno = models.BooleanField(default=False)
    n_jogadorRetorno = models.IntegerField()
    qt_jard_retorno = models.IntegerField()
    def_parou_jogada = models.BooleanField(default=False)
    jogador_parou_jogada = models.IntegerField()

    def __str__(self):
        return f"Punt do jogador {self.n_kicker}"

#####################################################################################################################
#SEGUE BASE MODEL DA TABELA FIELD GOAL
######################################################################################################################
class FieldGoal(models.Model):
    conclusaoJogada = models.ForeignKey(ConclusaoJogada, on_delete=models.CASCADE)
    n_kicker = models.IntegerField()
    resultado_jogada = models.CharField(max_length=50)
    posicao_campo = models.IntegerField()
    def_parou_jogada = models.BooleanField(default=False)
    jogador_parou_jogada = models.IntegerField()

    def __str__(self):
        return f"Field Goal do kicker {self.n_kicker}"