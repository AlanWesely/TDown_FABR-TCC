from django.urls import path
from . import views


app_name = 'games'

urlpatterns = [
    path('', views.home, name="home"),  # Acessa a Tela Home
    path('buscar/liga/<int:liga_id>/', views.liga, name="buscar-liga"),
    path('cadastro/partida/', views.cadastrar_partida, name='cadastro_partida'),  # Acessa Cad de Partida
    path('visualizar-partida/<id>/', views.viewPartida, name="viewPartida"),  # Acessa Vis Partida
    path('cadastro-jogada/<int:partida_id>/', views.cadJogada, name="cadJogada"),    # Acessa Tela Cad de Jogadas
    path('cadastro-time/', views.cadTime),  # Acessa a Tela Cadastro de Times
    path('detalhe-jogada/<int:jogada_id>/', views.detalhe_jogada, name='detalheJogada'),
    path('conclusao-jogada/<int:jogada_id>/', views.conclusao_jogada, name='conclusaoJogada'),
    path('logout/', views.logout_user, name='logout_user'),
    path('pagina-privada/', views.pagina_privada, name='pagina_privada'),
    path('login/', views.login_user, name='login_user')

]
