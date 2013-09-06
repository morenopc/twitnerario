# coding:utf8
import re
import random
import requests
from django.test import TestCase


class FuncoesTest(TestCase):
    """Nose testes para Funcoes"""

    fixtures = ['configuracao', 'registros']

    def test_registros(self):
        """Existem registros?"""
        try:
            from registros.models import Registros
        except ImportError:
            self.fail('Model registros nao existe')
        self.assertTrue(
            Registros.objects.all().exists(),
            msg='Não há registros no banco')

    def test_tweet(self):
        """O arquivo tweet existe?"""

        try:
            from core import tweet
        except ImportError:
            self.fail('O arquivo tweet nao existe')

    def test_previsao_key(self):
        """A chave foi encontrada e é válida?"""

        from core import tweet
        key = tweet.previsao_key()
        try:
            int(key)
        except ValueError:
            self.fail(u'Chave não encontrada ou inválida')

    def test_previsao_XML(self):
        """A previsao XML chegou e está correto?"""

        from registros.models import Registros
        from core import tweet

        regs = Registros.objects.all()
        reg = regs[random.randint(0, regs.count() - 1)]
        resposta = tweet.previsao(reg, tweet.previsao_key())
        # Status code
        self.assertEqual(resposta.status_code, 200,
            msg=u'Não foi possível obter o XML com a previsão')
        # Headers
        self.assertEqual(resposta.headers['content-type'],
            'application/xml;charset=UTF-8')

    def test_horarios(self):
        """Os horários foram obtidos?"""

        from registros.models import Registros
        from core import tweet
        # previsão XML
        regs = Registros.objects.all()
        reg = regs[random.randint(0, regs.count() - 1)]
        previsao = tweet.previsao(reg, tweet.previsao_key())
        previsao_xml = {reg.ponto: previsao.content}

        resposta = tweet.horarios(previsao_xml[reg.ponto],
            reg.linha)
        # É uma lista?
        self.assertTrue(isinstance(resposta, list))

    def test_tweet(self):
        """As mensages do tweets foram criadas?"""

        from registros.models import Registros
        from core import tweet
        # previsão XML
        regs = Registros.objects.all()
        reg = regs[random.randint(0, regs.count() - 1)]
        previsao = tweet.previsao(reg, tweet.previsao_key())
        previsao_xml = {reg.ponto: previsao.content}
        # obtem horarios
        horarios = tweet.horarios(previsao_xml[reg.ponto],
            reg.linha)

        resposta = tweet.tweet(
            reg.twitter, horarios, reg.linha)
        # É uma string?
        self.assertTrue(isinstance(resposta, str))
        # Contém a mensagem?
        self.assertNotEqual(len(resposta), 0)

    def test_create_tweets(self):
        """Os tweets foram criados?"""

        from registros.models import Registros
        from core import tweet

        qnt_restros = 5
        regs = Registros.objects.filter(id__lte=qnt_restros)
        resposta = tweet.create_tweets(regs)
        # É uma lista?
        self.assertTrue(isinstance(resposta, list))
        # Contém tweets?
        self.assertNotEqual(len(resposta), 0)
        # Contém todos os tweets?
        self.assertEqual(len(resposta), qnt_restros)
