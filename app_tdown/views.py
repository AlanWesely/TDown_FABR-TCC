from django.http import Http404
from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse
from utils.games.factory import make_game
from .models import Partida
# Create your views here.


def home(request):
    partida = Partida.objects.all().order_by('-id')
    return render(request, 'app_tdown/pages/home.html', context={
        'games': partida,
        'title': f'Home'
    })


def liga(request, liga_id):
    partida = get_list_or_404(
        Partida.objects.filter(
            divisoePartida__id=liga_id
        ).order_by('-id')
    )

    return render(request, 'app_tdown/pages/home.html', context={
        'games': partida,
        'title': f'{partida[0].divisoePartida.nomeEDivisao} - Liga'
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