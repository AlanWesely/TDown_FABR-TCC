from django.urls import path
from . import views


app_name = 'games'

urlpatterns = [
    path('', views.home, name="home"),     # Acessa a Tela Home
    path('cadastro-partida/<id>/', views.cadPartida, name="cadPartida"),  # Acessa Cad de Partida
    path('visualizar-partida/<id>/', views.viewPartida, name="viewPartida"),  # Acessa Vis Partida
    path('cadastro-jogada/', views.cadJogada, name="cadJogada"),    # Acessa Tela Cad de Jogadas
    path('cadastro-time/', views.cadTime)  # Acessa a Tela Cadastro de Times
]
