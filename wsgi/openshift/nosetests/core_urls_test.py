# coding:utf8
import re
import random
import requests
from django.test import TestCase
from django.utils import simplejson


class CoreUrlsTest(TestCase):
    """Nose testes para core urls"""
    
    fixtures = ['configuracao', 'registros']

    def test_localizar(self):
        """Os pontos foram localizados?"""

        resposta = self.client.get('/localizar/ /')
        self.assertEqual(resposta.status_code, 200,
            msg='GET {} {}'.format('/localizar/ /', resposta.status_code))
        # O JSON está correto?
        json = simplejson.loads(resposta.content)
        self.assertTrue(isinstance(json, dict))

    def test_pontos(self):
        """Retornou lista de pontos em JSON?"""

        resposta = self.client.get('/pontos/')
        self.assertEqual(resposta.status_code, 200,
            msg='GET {} {}'.format('/pontos/', resposta.status_code))
        # O JSON está correto?
        json = simplejson.loads(resposta.content)
        self.assertTrue(isinstance(json, dict))

    def test_pontos_local(self):
        """Retornou lista de pontos do arquivo em JSON?"""

        resposta = self.client.get('/pontos/local/')
        self.assertEqual(resposta.status_code, 200,
            msg='GET {} {}'.format('/pontos/local/', resposta.status_code))
        # O JSON está correto?
        json = simplejson.loads(resposta.content)
        self.assertTrue(isinstance(json, dict))

    def test_linhas(self):
        """Retornou linhas que passam no ponto em JSON?"""

        # Obtem pontos
        pontos = self.client.get('/pontos/')
        json = simplejson.loads(pontos.content)
        ponto = json['data'][
            random.randint(0, len(json['data']) - 1)].get('ponto')
        resposta = self.client.get('/ponto/{}/linhas/'.format(ponto))
        self.assertEqual(resposta.status_code, 200,
            msg='GET /ponto/{}/linhas/ {}'.format(ponto, resposta.status_code))
        # O JSON está correto?
        json = simplejson.loads(resposta.content)
        self.assertTrue(isinstance(json, dict))
