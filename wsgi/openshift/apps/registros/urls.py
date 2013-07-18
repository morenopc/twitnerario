# -*- coding: UTF8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('registros.views',
    url(r'^$', 'registro', name='registro'),
    url(r'^(?P<ponto>\d+)', 'registro_ponto', name='registro_ponto'),
)
