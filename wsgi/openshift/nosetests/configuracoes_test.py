# coding:utf8
import re
import random
import requests
from django.utils import simplejson
from django.test import TestCase


class ConfigTest(TestCase):
    """Nose testes"""

    fixtures = ['configuracao']

    def test_existe(self):
        """A configuracao existe?"""
        try:
            from apps.core.models import Configuracao
        except ImportError:
            self.fail('Model configuracao nao existe')

    def test_config_default(self):
        """A configuracao default existe?"""
        try:
            from apps.core.models import Configuracao
        except ImportError:
            self.fail('Model configuracao nao existe')
        self.assertTrue(
            Configuracao.objects.filter(
                descricao='default').exists(),
            msg='Configuracao default não foi localizada')

    def test_urls(self):
        """As urls da previsao funcionam?"""
        from apps.core.models import Configuracao
        url = Configuracao.objects.get(descricao='default')
        # Previsao origin
        origin = url.previsao_origin
        resposta = self.client.get(origin)
        self.assertEqual(resposta.status_code, 200,
            msg='GET {} {}'.format(origin, resposta.status_code))
        # Previsao javascript
        resposta = requests.get(origin + url.previsao_js)
        self.assertEqual(resposta.status_code, 200,
            msg=u'Não foi possível obter o JS com a chave da previsão')
        key = re.search(r'validar\|(\d+)\|success', resposta.content).group(1)
        # Lista de pontos JSON
        resposta = requests.get(origin + url.pontos_pathname)
        self.assertEqual(resposta.status_code, 200,
            msg=u'Não foi possível obter a lista de pontos')
        pontos = simplejson.loads(resposta.content)
        ponto = pontos['data'][
            random.randint(0, len(pontos['data']) - 1)].get('ponto')
        # Linha JSON
        resposta = requests.get(
            origin + url.linhas_pathname,
            params={'ponto_oid': ponto})
        self.assertEqual(resposta.status_code, 200,
            msg=u'Não foi possível obter linha(s)')
        linhas = simplejson.loads(resposta.content)
        linha = linhas['data'][
            random.randint(0, len(linhas['data']) - 1)].get('linha')
        # Previsao pathname
        headers = {
            'Referer': 'http://rast.vitoria.es.gov.br/pontovitoria/',
            'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64) '
                    'AppleWebKit/537.11 (KHTML, like Gecko) '
                    'Chrome/23.0.1271.95 Safari/537.11')
        }
        payload = {'ponto': ponto, 'linha': linha.split()[0], 'key': key}
        resposta = requests.get(
            origin + url.previsao_pathname,
            params=payload,
            headers=headers)
        self.assertEqual(resposta.status_code, 200,
            msg=u'Não foi possível obter o XML com a previsão')
