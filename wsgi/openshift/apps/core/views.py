# -*- coding: UTF8 -*-
import requests
from django.utils import simplejson
from django.conf import settings
from django.utils.encoding import smart_str
from apps.core.models import Configuracao
from django.http import HttpResponse
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from core.tweet import previsao_key, previsao_xml, horarios

    
def pesquisar(request):
    """
    Busca por pontos com base na referência e retorna json
    """
    pontos = {}
    s = request.GET.get('s', None)
    if s:
        url = Configuracao.objects.get(descricao='default')
        resposta = requests.get(url.previsao_origin + url.pontos_pathname,
                params={'referencia': s})
        pontos = simplejson.loads(resposta.content)

    return render_to_response('registros/pontos-pesquisar.html',
        context_instance=RequestContext(request, {'pontos': pontos}))


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
        open('{}{}json/listaPontos.json'.format(
            settings.PROJECT_DIR, settings.MEDIA_URL)).read(),
        mimetype='application/json')


def linhas(request, ponto):
    """
    Retorna linhas que passam no ponto
    """
    url = Configuracao.objects.get(descricao='default')
    resposta = requests.get(url.previsao_origin + url.linhas_pathname,
            params={'ponto_oid': ponto})
    context = {
        'ponto': ponto,
        'linhas': simplejson.loads(resposta.content)
    }
    return render_to_response('registros/linhas-ponto.html',
        context_instance=RequestContext(request, context))


def linhas_json(request, ponto):
    """
    Retorna linhas que passam no ponto
    """
    url = Configuracao.objects.get(descricao='default')
    resposta = requests.get(url.previsao_origin + url.linhas_pathname,
            params={'ponto_oid': ponto})
    return HttpResponse(resposta.content,
        mimetype='application/json')


def previsoes(request, ponto, linha):
    """
    Retorna horarios
    """
    xml = previsao_xml(ponto, linha, previsao_key())
    hs = horarios(xml.content, linha)
    hs.sort()
    
    context = {
        'ponto': ponto,
        'linha': linha,
        'horarios': hs
    }
    return render_to_response('registros/horarios-linha.html',
        context_instance=RequestContext(request, context))