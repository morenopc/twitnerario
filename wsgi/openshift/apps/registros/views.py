# -*- coding: UTF8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext
from registros.models import Registros
from registros.forms import RegistrosForm
from django.http import HttpResponse, HttpResponseRedirect


def pesquisar(request):
    """Página inicial de pesquisa de pontos"""
    
    return render_to_response('pesquisar/pesquisar.ponto.html',
        context_instance=RequestContext(request))


def registrar(request):
    """
    Recebe formulário e registra tweet
    """

    form = RegistrosForm(request.POST or None)
    if form.is_valid():
        form.save()
        context = {
            'twitter': request.POST['twitter'],
            'h': request.POST['horas'],
            'm': request.POST['minutos']
        }
        return render_to_response('registros/sucesso.html',
            context_instance=RequestContext(request,context))

    return render_to_response('registros/registro.html',
        context_instance=RequestContext(request, {'form': form}))


def registrar_ponto(request, ponto):
    """
    Recebe número do ponto e preenche o formulário
    """

    form = RegistrosForm(initial={'ponto': ponto})
    if request.method == 'POST':
        form = RegistrosForm(request.POST)
        if form.is_valid():
            form.save()
            context = {
                'twitter': request.POST['twitter'],
                'h': request.POST['horas'],
                'm': request.POST['minutos']
            }
            return render_to_response('registros/sucesso.html',
                context_instance=RequestContext(request,context))

    return render_to_response('registros/registro.html',
        context_instance=RequestContext(request, {'form': form}))
