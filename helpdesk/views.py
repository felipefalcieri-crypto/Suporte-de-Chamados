from django.shortcuts import render, get_object_or_404, redirect
from .models import Chamado
from .forms import ChamadoAtualizacaoForm, ChamadoForm
from django.utils import timezone
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required


def obter_contadores():
    chamados_abertos = Chamado.objects.filter(
        status__in=['NOVO', 'ANDAMENTO', 'PENDENTE']
    )
    contadores = chamados_abertos.aggregate(
        abertos=Count('id'),
        novos=Count('id', filter=Q(status='NOVO')),
        em_andamento=Count('id', filter=Q(status='ANDAMENTO')),
        pendentes=Count('id', filter=Q(status='PENDENTE')),
    )
    return contadores


def vizualizarHome(request):
    contadores = obter_contadores()
    chamados_abertos_lista = Chamado.objects.filter(
        status__in=['NOVO', 'ANDAMENTO', 'PENDENTE']
    ).order_by('-data_abertura')

    context = {
        'contador': contadores,
        'chamados_alta': chamados_abertos_lista,
    }
    return render(request, 'home.html', context)


def ticketsAbertos(request):
    contadores = obter_contadores()
    chamados_base = Chamado.objects.all().order_by('-data_abertura')
    ver_fechados = request.GET.get('ver_fechados', 'nao')

    if ver_fechados == 'sim':
        chamados_listados = chamados_base
    elif ver_fechados == 'apenas_fechados':
        chamados_listados = chamados_base.filter(status='FECHADO')
    else:
        chamados_listados = chamados_base.exclude(status='FECHADO')

    filtro = request.GET.get('filtro', 'todos')

    if filtro == 'novo':
        chamados_filtrados = chamados_listados.filter(status='NOVO')
    elif filtro == 'pendente':
        chamados_filtrados = chamados_listados.filter(status='PENDENTE')
    elif filtro == 'andamento':
        chamados_filtrados = chamados_listados.filter(status='ANDAMENTO')
    else:
        chamados_filtrados = chamados_listados

    context = {
        'chamados': chamados_filtrados,
        'filtro_ativo': filtro,
        'ver_fechados_ativo': ver_fechados,
        'contador': contadores,
    }

    return render(request, 'tickets_abertos.html', context)


def detalhe_ticket(request, chamado_id):
    chamado = get_object_or_404(Chamado, pk=chamado_id)
    form = ChamadoAtualizacaoForm(instance=chamado)
    contadores = obter_contadores()

    context = {
        'chamado': chamado,
        'form': form,
        'contador': contadores,
    }
    return render(request, 'detalhe_ticket.html', context)


def atualizar_chamado(request, chamado_id):
    chamado = get_object_or_404(Chamado, pk=chamado_id)

    if request.method == 'POST':
        form = ChamadoAtualizacaoForm(request.POST, instance=chamado)
        if form.is_valid():
            chamado = form.save(commit=False)

            if chamado.status == 'CONCLUIDO' and not chamado.data_encerramento:
                chamado.data_encerramento = timezone.now()
            elif chamado.status != 'CONCLUIDO':
                chamado.data_encerramento = None

            chamado.save()
            return redirect('detalhe_ticket', chamado_id=chamado.id)

    return redirect('detalhe_ticket', chamado_id=chamado.id)


@login_required
def abertura_chamado(request):
    contadores = obter_contadores()

    if request.method == 'POST':
        form = ChamadoForm(request.POST)
        if form.is_valid():
            novo_chamado = form.save(commit=False)

            novo_chamado.solicitante = request.user
            novo_chamado.status = 'ANDAMENTO'

            novo_chamado.save()

            return redirect('detalhe_ticket', chamado_id=novo_chamado.pk)

    else:
        form = ChamadoForm()

    context = {
        'form': form,
        'contador': contadores,
    }

    return render(request, 'abertura_chamado.html', context)
