from django.shortcuts import render, redirect
from perfil.models import Categoria
from .models import ContaPagar, ContaPaga
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime

# Create your views here.
def definir_contas(request):
    if request.method == "GET":
        categorias = Categoria.objects.all()
        return render(request, 'definir_contas.html', {'categorias':categorias})
    else:
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        dia_pagamento = request.POST.get('dia_pagamento')

        conta = ContaPagar(
            titulo=titulo,
            categoria_id=categoria,
            descricao=descricao,
            valor=valor,
            dia_pagamento=dia_pagamento
        )

        conta.save()

        messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com Sucesso!')

        return redirect('/contas/definir_contas')
    

def ver_contas(request):
    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day
    
    contas = ContaPagar.objects.all()

    contas_pagas = ContaPaga.objects.filter(data_pagamento__month=MES_ATUAL).values('conta')
    pagas = len(contas_pagas)

    contas_vencidas = contas.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=contas_pagas)
    vencidas = len(contas_vencidas)

    contas_proximas_vencimento = contas.filter(dia_pagamento__lte = DIA_ATUAL + 5).filter(dia_pagamento__gte=DIA_ATUAL).exclude(id__in=contas_pagas)
    proximas = len(contas_proximas_vencimento)

    restantes = contas.exclude(id__in=contas_vencidas).exclude(id__in=contas_pagas).exclude(id__in=contas_proximas_vencimento)
    contas_restantes =len(restantes)

    return render(request, 'ver_contas.html', {'pagas':pagas, 'vencidas':vencidas, 'proximas':proximas, 'contas_restantes':contas_restantes, 'contas_vencidas': contas_vencidas, 'contas_proximas_vencimento': contas_proximas_vencimento, 'restantes': restantes})


def update_pagar(request, id):
    conta = ContaPaga.objects.all()
    
    conta = ContaPaga(
        conta_id=id,
        data_pagamento = datetime.now()
    )
    
    conta.save()

    return redirect('/contas/ver_contas')
