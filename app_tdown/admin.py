from django.contrib import admin
from .models import Time, Liga, Modalidade, Federacoes, DivisoesCampeonatos, Partida, Jogada, Falta, FaltaCometida, Pontuacao, ConclusaoJogada, Passe, Punt, Corrida, FieldGoal

# Register your models here.
class TimeAdmin(admin.ModelAdmin):
    ...

admin.site.register(Time, TimeAdmin)

@admin.register(Liga)
class LigaAdmin(admin.ModelAdmin):
    ...

@admin.register(Modalidade)
class ModalidadeAdmin(admin.ModelAdmin):
    ...

@admin.register(Federacoes)
class FederacaoAdmin(admin.ModelAdmin):
    ...

@admin.register(DivisoesCampeonatos)
class DivisaoAdmin(admin.ModelAdmin):
    ...

@admin.register(Partida)
class PartidaAdmin(admin.ModelAdmin):
    ...

@admin.register(Jogada)
class JogadaAdmin(admin.ModelAdmin):
    ...

@admin.register(Falta)
class FaltaAdmin(admin.ModelAdmin):
    ...

@admin.register(FaltaCometida)
class FaltaCometidaAdmin(admin.ModelAdmin):
    ...

@admin.register(Pontuacao)
class PontuacaoAdmin(admin.ModelAdmin):
    ...

@admin.register(ConclusaoJogada)
class ConclusaoJogadaAdmin(admin.ModelAdmin):
    ...

@admin.register(Passe)
class PasseAdmin(admin.ModelAdmin):
    ...

@admin.register(Punt)
class PuntAdmin(admin.ModelAdmin):
    ...

@admin.register(FieldGoal)
class FieldGoalAdmin(admin.ModelAdmin):
    ...

@admin.register(Corrida)
class CorridaAdmin(admin.ModelAdmin):
    ...