# coding:utf8
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Configuracao(models.Model):
    """
        Registro das configurações e urls usadas para receber as previsões
        (xml e outros) do serviço ponto vitória
    """

    class Meta:
        verbose_name = _(u'configuração')
        verbose_name_plural = _(u'configurações')

    descricao = models.CharField(_(u'configuração'), max_length=128,
        default='default')
    previsao_origin = models.URLField(_(u'ponto vitória url'),
        max_length=128, default='http://rast.vitoria.es.gov.br/')
    previsao_pathname = models.CharField(
        _(u'previsão'), max_length=128, default='pontovitoria/previsao?')
    previsao_js = models.CharField(
        _(u'previsão javascript'), max_length=128,
        default='pontovitoria/js/principal/previsao.js')
    pontos_pathname = models.CharField(
        _(u'lista de pontos'), max_length=128,
        default='pontovitoria/utilidades/listaPontos/')
    linhas_pathname = models.CharField(
        _(u'linhas que passam no ponto'), max_length=128,
        default='pontovitoria/utilidades/listaLinhaPassamNoPonto/')

    def __unicode__(self):
        return u'{}'.format(self.descricao)
