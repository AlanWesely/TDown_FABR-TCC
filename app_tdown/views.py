from django.http import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.http import HttpResponse
from utils.games.factory import make_game
from .models import Partida, Jogada
from .forms import PartidaForm, JogadaForm
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

#######################################################################################################################################################/
#CADASTRO FORMS CADASTRO JOGADAS
###########################################################################################################################################
def cadJogada(request, id):
    partida = get_object_or_404(Partida, pk=id)
    jogadas = Jogada.objects.filter(partida=partida).order_by('jogada')
    proxima_jogada = jogadas.count() + 1
    tempo_atual = jogadas.last().tempo if jogadas.exists() else 1

    if request.method == 'POST':
        form = JogadaForm(request.POST)
        if form.is_valid():
            nova_jogada = form.save(commit=False)
            nova_jogada.partida = partida
            nova_jogada.jogada = proxima_jogada
            nova_jogada.tempo = int(request.POST.get('tempo'))
            nova_jogada.descida = int(request.POST.get('descida'))
            print("tempo:", request.POST.get("tempo"))
            print("descida:", request.POST.get("descida"))
            nova_jogada.timeDefendendo = (
                partida.timeVisitante if nova_jogada.timeAtacando == partida.timeCasa
                else partida.timeCasa
            )
            nova_jogada.save()
            return redirect('games:conclusaoJogada', jogada_id=nova_jogada.id)
    else:
        form = JogadaForm(initial={
            'partida': partida,
            'jogada': proxima_jogada,
            'tempo': tempo_atual,
        })

    return render(request, 'app_tdown/pages/cadJogadas.html', {
        'form': form,
        'partida': partida,
        'jogadas': jogadas,
        'proxima_jogada': proxima_jogada,
        'tempo': tempo_atual,
    })

#######################################################################################################################################################

def cadTime(request):
    return HttpResponse('cadTime')  # Cadastro das Times

#######################################################################################################################################################
#CADASTRO FORMS CONCLUSÃO DA JOGADA
#######################################################################################################################################################
def conclusao_jogada(request, jogada_id):
    jogada = get_object_or_404(Jogada, pk=jogada_id)

    return render(request, 'app_tdown/pages/conclusaoJogada.html', {
        'jogada': jogada,
    })
