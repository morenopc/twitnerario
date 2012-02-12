# -*- coding: UTF8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('registros.views',
    url(r'^$', 'registro', name='registro'),
)
