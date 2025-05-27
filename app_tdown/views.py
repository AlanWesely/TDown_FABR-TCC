from django.http import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.http import HttpResponse
from utils.games.factory import make_game
from .models import Partida
from .forms import PartidaForm
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



#def cadPartida(request, id):
#    return render(request, 'app_tdown/pages/cadPartida.html', context={
#        'game': make_game(),
#    })  # Cadastro de Partida

###########################################################################################################################################
#CADASTRO FORMS PARTIDA
###########################################################################################################################################
def cadastrar_partida(request):
    if request.method == 'POST':
        form = PartidaForm(request.POST, request.FILES)
        if form.is_valid():
            partida = form.save(commit=False)

            timeCasa = partida.timeCasa.nomeAbreviado
            timeVisitante = partida.timeVisitante.nomeAbreviado
            liga = partida.ligaPartida.nomeAbrevLiga
            partida.nomePartida = f"{timeCasa} x {timeVisitante} - {liga}"

            partida.save()
            return render(request, 'app_tdown/pages/sucessoPartida.html', {'partida': partida})

    else:
        form = PartidaForm()

    return render(request, 'app_tdown/pages/cadPartida.html', {'form': form})

###########################################################################################################################################


def viewPartida(request, id):
    partida = get_object_or_404(Partida, pk=id)

    return render(request, 'app_tdown/pages/viewPartida.html', context={
        'game': partida,
        'is_detail_page': True,
        'title': f'{partida.nomePartida} - Partida'
    })  # Cadastro de Partida


def cadJogada(request):
    return render(request, 'app_tdown/pages/cadJogadas.html', context={
        'game': make_game(),
    })   # Cadastro das Jogadas


def cadTime(request):
    return HttpResponse('cadTime')  # Cadastro das Times