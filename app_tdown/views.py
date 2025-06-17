from django.http import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.http import HttpResponse
from utils.games.factory import make_game
from .models import Partida, Jogada, ConclusaoJogada, Pontuacao, FaltaCometida, Falta, Corrida, FieldGoal, Punt, Passe
from .forms import PartidaForm, JogadaForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


def home(request):
    partida = Partida.objects.all().order_by('-id')
    return render(request, 'app_tdown/pages/home.html', context={
        'games': partida,
        'is_home': True,
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

def logout_user(request):
    logout(request)
    return redirect('games:home')


@login_required(login_url='games:login_user')  # Redireciona para a tela de login se não estiver logado
def pagina_privada(request):
    return render(request, 'app_tdown/pages/pagina_privada.html')

#def cadPartida(request, id):
#    return render(request, 'app_tdown/pages/cadPartida.html', context={
#        'game': make_game(),
#    })  # Cadastro de Partida

###########################################################################################################################################
#CADASTRO FORMS PARTIDA
###########################################################################################################################################
@login_required(login_url='games:login_user')
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
        'is_home': False,
        'title': f'{partida.nomePartida} - Partida'
    })  # Cadastro de Partida

###########################################################################################################################################
#CADASTRO FORMS CADASTRO JOGADAS
###########################################################################################################################################
def cadJogada(request, partida_id):
    partida = get_object_or_404(Partida, pk=partida_id)
    jogadas = Jogada.objects.filter(partida=partida).order_by('jogada')
    proxima_jogada = jogadas.count() + 1
    tempo_atual = jogadas.last().tempo if jogadas.exists() else 1

    # CALCULAR PLACAR
    conclusoes = ConclusaoJogada.objects.filter(jogada__partida=partida).select_related('jogada', 'tipoPontuacao')
    pontuacoes_dict = {
        'Touchdown': 6,
        'Field Goal': 3,
        'Extra Point': 1,
        'Mini Touchdown': 1,
        'Safety': 2,
    }
    placar = {'casa': 0, 'visitante': 0}

    for conclusao in conclusoes:
        tipo = conclusao.tipoPontuacao.nomePontuacao if conclusao.tipoPontuacao else None
        if tipo:
            pontos = pontuacoes_dict.get(tipo, 0)
            atacante = conclusao.jogada.timeAtacando
            if tipo == 'Safety':
                lado = 'casa' if atacante == partida.timeVisitante else 'visitante'
            else:
                lado = 'casa' if atacante == partida.timeCasa else 'visitante'
            placar[lado] += pontos


    # FORMULÁRIO
    if request.method == 'POST':
        form = JogadaForm(request.POST)
        if form.is_valid():
            nova_jogada = form.save(commit=False)
            nova_jogada.partida = partida
            nova_jogada.jogada = proxima_jogada
            nova_jogada.timeDefendendo = (
                partida.timeVisitante if nova_jogada.timeAtacando == partida.timeCasa
                else partida.timeCasa
            )
            nova_jogada.save()
            # 👇 Redireciona para a conclusão
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
        'placar': placar,
        'is_home': False,
    })


#######################################################################################################################################################
@login_required(login_url='games:login_user')
def cadTime(request):
    return HttpResponse('cadTime')  # Cadastro das Times

#######################################################################################################################################################
#CADASTRO FORMS CONCLUSÃO DA JOGADA
#######################################################################################################################################################
@login_required(login_url='games:login_user')
def conclusao_jogada(request, jogada_id):
    jogada = get_object_or_404(Jogada, pk=jogada_id)
    partida = jogada.partida
    pontuacoes = Pontuacao.objects.all()
    tipos_jogada = ["Passe", "Corrida", "Punt", "Field Goals", "Kickoff"]  # 👈 MOVA AQUI PRA CIMA

    if request.method == 'POST':
        tipoJogada = request.POST.get('tipoJogada')
        possuiFalta = bool(request.POST.get('possuiFalta'))
        jogPossuiFumble = bool(request.POST.get('jogPossuiFumble'))
        timeAtaqueRecuperou = bool(request.POST.get('timeAtaqueRecuperou'))
        jogadaComPontuacao = bool(request.POST.get('jogadaComPontuacao'))
        tipoPontuacao_id = request.POST.get('tipoPontuacao')

        tipoPontuacao = Pontuacao.objects.get(pk=tipoPontuacao_id) if tipoPontuacao_id else None

        ConclusaoJogada.objects.create(
            jogada=jogada,
            tipoJogada=tipoJogada,
            possuiFalta=possuiFalta,
            jogPossuiFumble=jogPossuiFumble,
            timeAtaqueRecuperou=timeAtaqueRecuperou,
            jogadaComPontuacao=jogadaComPontuacao,
            tipoPontuacao=tipoPontuacao
        )

        return redirect('games:detalheJogada', jogada_id=jogada.id)

    return render(request, 'app_tdown/pages/conclusaoJogada.html', {
        'jogada': jogada,
        'partida': partida,
        'pontuacoes': pontuacoes,
        'tipos_jogada': tipos_jogada,
        'is_home': False,
    })




#######################################################################################################################################################
#CADASTRO FORMS DETALHE JOGADA
#######################################################################################################################################################
@login_required(login_url='games:login_user')
def detalhe_jogada(request, jogada_id):
    jogada = get_object_or_404(Jogada, pk=jogada_id)
    partida = jogada.partida
    conclusao = ConclusaoJogada.objects.filter(jogada=jogada).last()
    faltas = FaltaCometida.objects.filter(conclusaoJogada__jogada__partida=partida).order_by('conclusaoJogada__jogada__jogada')
    corridas = Corrida.objects.filter(conclusaoJogada=conclusao)
    todas_faltas = Falta.objects.all()

    # Opções de campos de corrida
    resultado_corrida_opcoes = ["Concluida", "Corrida Interrompida", "Fumble"]
    direcao_corrida_opcoes = ["Direita", "Esquerda"]
    gap_corrida_opcoes = ["1", "2", "3", "4", "5", "6", "7"]

    # Opções de campos de passe
    resultado_passe_opcoes = ["Concluido", "Passe Incompleto", "Interceptado"]
    direcao_passe_opcoes = ["Direita", "Centro", "Esquerda"]
    profundidade_passe_opcoes = ["Curto", "Médio", "Longo"]

    # Opção de campos de Punt
    resultado_punt_opcoes = ["Fair Catch", "Touchback", "Coffin Corner", "Fumble", "Fake Punt"]

    # Opção de campos de Punt
    resultado_fielGoal_opcoes = ["Chute Convertido", "Chute Bloqueado", "Chute Desviado", "Field Goal Fake"]

    if request.method == 'POST':
        if 'registrar_falta' in request.POST:
            tipoFalta_id = request.POST.get('tipoFalta')
            timeCometeuFalta_id = request.POST.get('timeCometeuFalta')
            num_jogador = request.POST.get('num_jogadorFezFalta')

            FaltaCometida.objects.create(
                conclusaoJogada=conclusao,
                tipoFalta_id=tipoFalta_id,
                timeCometeuFalta_id=timeCometeuFalta_id,
                num_jogadorFezFalta=num_jogador
            )
            return redirect('games:detalheJogada', jogada_id=jogada.id)

        elif 'registrar_corrida' in request.POST:
            n_quaterback = request.POST.get('n_quaterback')
            n_corredor = request.POST.get('n_corredor')
            resultado_jogada = request.POST.get('resultado_jogada')
            direcao_corrida = request.POST.get('direcao_corrida')
            qt_jard_percorreu = request.POST.get('qt_jard_percorreu')
            gap_corrida = request.POST.get('gap_corrida')
            def_parou_jogada = bool(request.POST.get('def_parou_jogada'))
            jogador_parou_jogada = request.POST.get('jogador_parou_jogada') or None

            Corrida.objects.create(
                conclusaoJogada=conclusao,
                n_quaterback=n_quaterback,
                n_corredor=n_corredor,
                resultado_jogada=resultado_jogada,
                direcao_corrida=direcao_corrida,
                qt_jard_percorreu=qt_jard_percorreu,
                gap_corrida=gap_corrida,
                def_parou_jogada=def_parou_jogada,
                jogador_parou_jogada=jogador_parou_jogada
            )
            return redirect('games:cadJogada', partida_id=partida.id)

        elif 'registrar_fieldgoal' in request.POST:
            FieldGoal.objects.create(
                conclusaoJogada=conclusao,
                n_kicker=request.POST.get('n_kicker'),
                resultado_jogada=request.POST.get('resultado_jogada'),
                posicao_campo=request.POST.get('posicao_campo'),
                def_parou_jogada=bool(request.POST.get('def_parou_jogada')),
                jogador_parou_jogada=request.POST.get('jogador_parou_jogada') or None
            )
            return redirect('games:cadJogada', partida_id=partida.id)

        elif 'registrar_punt' in request.POST:
            Punt.objects.create(
                conclusaoJogada=conclusao,
                n_kicker=request.POST.get('n_kicker'),
                resultado_jogada=request.POST.get('resultado_jogada'),
                posicao_campo=request.POST.get('posicao_campo'),
                qt_jard_punt=request.POST.get('qt_jard_punt'),
                teve_retorno=bool(request.POST.get('teve_retorno')),
                n_jogadorRetorno=request.POST.get('n_jogadorRetorno') or None,
                qt_jard_retorno=request.POST.get('qt_jard_retorno') or None,
                def_parou_jogada=bool(request.POST.get('def_parou_jogada')),
                jogador_parou_jogada=request.POST.get('jogador_parou_jogada') or None
            )
            return redirect('games:cadJogada', partida_id=partida.id)

        elif 'registrar_passe' in request.POST:
            Passe.objects.create(
                conclusaoJogada=conclusao,
                n_quaterback=request.POST.get('n_quaterback'),
                n_recebedor=request.POST.get('n_recebedor'),
                resultado_jogada=request.POST.get('resultado_jogada'),
                direcao_passe=request.POST.get('direcao_passe'),
                qt_jard_percorreu=request.POST.get('qt_jard_percorreu'),
                profundidade_passe=request.POST.get('profundidade_passe'),
                def_parou_jogada=bool(request.POST.get('def_parou_jogada')),
                jogador_parou_jogada=request.POST.get('jogador_parou_jogada') or None
            )
            return redirect('games:cadJogada', partida_id=partida.id)

    return render(request, 'app_tdown/pages/detalheJogada.html', {
        'jogada': jogada,
        'partida': partida,
        'conclusao': conclusao,
        'faltas_cometidas': faltas,
        'corridas': corridas,
        'todas_faltas': todas_faltas,
        'resultado_corrida_opcoes': resultado_corrida_opcoes,
        'direcao_corrida_opcoes': direcao_corrida_opcoes,
        'gap_corrida_opcoes': gap_corrida_opcoes,
        'resultado_passe_opcoes': resultado_passe_opcoes,
        'direcao_passe_opcoes': direcao_passe_opcoes,
        'profundidade_passe_opcoes': profundidade_passe_opcoes,
        'resultado_punt_opcoes' : resultado_punt_opcoes,
        'resultado_fielGoal_opcoes' : resultado_fielGoal_opcoes,
        'is_home': False,
    })

#######################################################################################################################################################
#CADASTRO FORMS LOGIN USER
#######################################################################################################################################################
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login com sucesso!')
            return redirect('games:home')  # ou o nome correto da sua view de home
        else:
            messages.error(request, 'Usuário ou senha incorretos.')

    return render(request, 'app_tdown/pages/login.html')