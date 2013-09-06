# coding:utf8
import re
import random
import requests
from django.test import TestCase
from django.utils import simplejson


class CoreUrlsTest(TestCase):
    """Nose testes para core urls"""
    
    fixtures = ['configuracao']

    def test_pesquisar(self):
        """Abre a página de pesquisa?"""

        resposta = self.client.get('/')
        self.assertEqual(resposta.status_code, 200,
            msg='GET {} {}'.format('/', resposta.status_code))

    def test_registrar(self):
        """Abre a página de registro de tweet?"""
        # GET
        resposta = self.client.get('/registro/')
        self.assertEqual(resposta.status_code, 200,
            msg='GET {} {}'.format('/registro/', resposta.status_code))
        
    def test_registrar_POST(self):
        """Registra tweet?"""
        # POST
        resposta = self.client.post('/registro/',
            {
                'twitter': '@morenocunha',
                'linha': '121',
                'ponto': '2137',
                'horas': 20,
                'minutos': 15
            })
        self.assertEqual(resposta.status_code, 200,
            msg='POST {} {}'.format('/registro/', resposta.status_code))

    def test_registrar_ponto(self):
        """Abre a página de registro de tweet com ponto?"""
        # Obtem ponto
        pontos = self.client.get('/pontos/')
        json = simplejson.loads(pontos.content)
        ponto = json['data'][
            random.randint(0, len(json['data']) - 1)].get('ponto')
        # GET
        resposta = self.client.get('/registro/{}/ponto/'.format(ponto))
        self.assertEqual(resposta.status_code, 200,
            msg='GET /registro/{}/ponto/ {}'.format(
                ponto, resposta.status_code))
        
    def test_registrar_ponto_POST(self):
        """Registra tweet com ponto?"""
        # Obtem ponto
        pontos = self.client.get('/pontos/')
        json = simplejson.loads(pontos.content)
        ponto = json['data'][
            random.randint(0, len(json['data']) - 1)].get('ponto')
        # POST
        resposta = self.client.post('/registro/{}/ponto/'.format(ponto),
            {
                'twitter': '@morenocunha',
                'linha': '121',
                'ponto': ponto,
                'horas': 20,
                'minutos': 15
            })
        self.assertEqual(resposta.status_code, 200,
            msg='POST /registro/{}/ponto/ {}'.format(
                ponto, resposta.status_code))
