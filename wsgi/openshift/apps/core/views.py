# -*- coding: UTF8 -*-
import requests
from django.conf import settings
from django.utils.encoding import smart_str
from apps.core.models import Configuracao
from django.http import HttpResponse


def localizar(request, ref):
    """
    Busca por pontos com base na referência
    """
    url = Configuracao.objects.get(descricao='default')
    resposta = requests.get(url.previsao_origin + url.pontos_pathname,
            params={'referencia': smart_str(ref)})
    return HttpResponse(resposta.content,
        mimetype='application/json')


def pontos(request):
    """
    Retortna lista de pontos json
    """
    url = Configuracao.objects.get(descricao='default')
    resposta = requests.get(url.previsao_origin + url.pontos_pathname)
    return HttpResponse(resposta.content,
        mimetype='application/json')


def pontos_local(request):
    """
    Retortna lista de pontos do arquivo json
    """
    return HttpResponse(
        open(settings.PROJECT_DIR + '/media/json/listaPontos.json').read(),
        mimetype='application/json')


def linhas(request, ponto):
    """
    Retorna linhas que passam no ponto
    """
    url = Configuracao.objects.get(descricao='default')
    resposta = requests.get(url.previsao_origin + url.linhas_pathname,
            params={'ponto_oid': ponto})
    return HttpResponse(resposta.content,
        mimetype='application/json')
