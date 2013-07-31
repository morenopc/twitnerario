# coding:utf8
from django.test import TestCase


class ConfigTest(TestCase):
    """Nose testes"""
        
    def test_existe(self):
        """ A conguracao existe? """
        try:
            from apps.core.models import Configuracao
        except ImportError:
            self.fail('Model configuracao nao existe')
