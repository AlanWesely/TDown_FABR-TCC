from django import forms
from .models import Partida, Time, Liga, DivisoesCampeonatos, Modalidade, Jogada

class PartidaForm(forms.ModelForm):
    timeCasa = forms.ModelChoiceField(queryset=Time.objects.all(), label="Time da Casa")
    timeVisitante = forms.ModelChoiceField(queryset=Time.objects.all(), label="Time Visitante")
    dataPartida = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Data da Partida")
    horarioPartida = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label="Horário da Partida")
    divisoePartida = forms.ModelChoiceField(queryset=DivisoesCampeonatos.objects.all(), label="Divisão")
    ligaPartida = forms.ModelChoiceField(queryset=Liga.objects.all(), label="Liga")
    modalidadePartida = forms.ModelChoiceField(queryset=Modalidade.objects.all(), label="Modalidade")
    logoPartida = forms.ImageField(label="Logo da Partida")

    class Meta:
        model = Partida
        exclude = ['nomePartida']


class JogadaForm(forms.ModelForm):
    class Meta:
        model = Jogada
        fields = ['tempo', 'descida', 'timeAtacando', 'jardaFirst', 'posicaoBola']
