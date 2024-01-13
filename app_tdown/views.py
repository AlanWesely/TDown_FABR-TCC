from django.shortcuts import render
from django.http import HttpResponse
from utils.games.factory import make_game
# Create your views here.


def home(request):
    return render(request, 'app_tdown/pages/home.html', context={
        'games': [make_game() for _ in range(10)],
    })


def cadPartida(request, id):
    return render(request, 'app_tdown/pages/cadPartida.html', context={
        'game': make_game(),
    })  # Cadastro de Partida


def viewPartida(request, id):
    return render(request, 'app_tdown/pages/viewPartida.html', context={
        'game': make_game(),
        'is_detail_page': True,
    })  # Cadastro de Partida


def cadJogada(request):
    return render(request, 'app_tdown/pages/cadJogadas.html', context={
        'game': make_game(),
    })   # Cadastro das Jogadas


def cadTime(request):
    return HttpResponse('cadTime')  # Cadastro das Times