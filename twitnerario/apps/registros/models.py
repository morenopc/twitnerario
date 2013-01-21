# -*- coding: UTF8 -*-

from django.db import models
from registros.model_choices import HORAS, MINUTOS, LEMBRAR


class Registros(models.Model):
    """
    Você será mencionado em um tweet (@twitnerario)
    com o horário aproximado do seu ônibus.
    """
    criado_em = models.DateTimeField('criado em', auto_now_add=True)
    twitter = models.CharField('twitter', max_length=15)
    ponto = models.CharField(u'ponto', max_length=4)
    linha = models.CharField(u'linha', max_length=6)
    horas = models.PositiveSmallIntegerField(u'quero ser lembrado às',
        choices=HORAS, default=7)
    minutos = models.PositiveSmallIntegerField(u':', choices=MINUTOS,
        default=0)
    lembrar = models.PositiveSmallIntegerField(u'me lembre',
        choices=LEMBRAR, default=0)
    fim_de_semana = models.BooleanField(u'incluir fim de semana?',
        default=False)
    falhou = models.BooleanField(u'falhou?', default=False)

    class Meta:
        verbose_name = u"Registro"

    def __unicode__(self):
        return '@{0} {1} {2}:{3}'.format(self.twitter, self.linha,
            self.horas, self.minutos)
