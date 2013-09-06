# -*- coding: UTF8 -*-
from django.conf.urls import *

urlpatterns = patterns('registros.views',
    url(r'^$', 'registrar', name='registrar'),
    url(r'^(?P<ponto>\d+)/ponto/$', 'registrar_ponto',
    	name='registrar_ponto'),
)
