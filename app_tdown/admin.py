from django.contrib import admin
from .models import Time, Liga, Modalidade, Federacoes, DivisoesCampeonatos, Partida

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