# -*- coding: UTF8 -*-
from django.conf.urls import *
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.conf import settings
from django.contrib import admin
admin.autodiscover()


# includes
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)
# Core Tweet
urlpatterns += patterns('apps.core.views',
    url(r'^$', 'pesquisar', name='pesquisar'),
    # Ponto Vitória fora do ar
    url(r'^(\w+)/$',
        RedirectView.as_view(
            url=('http://vitoria.es.gov.br/noticia/'
                'ponto-vitoria-passa-por-atualizacao-e-modernizacao-15798'),
            permanent=False),
        name='out-of-service'),

    url(r'^pesquisar', 'pesquisar', name='pesquisar'),
    url(r'^pontos/$', 'pontos', name='pontos'),
    url(r'^pontos/local/$', 'pontos_local', name='pontos_local'),
    url(r'^ponto/(?P<ponto>\d+)/linhas/$', 'linhas', name='linhas'),
    url(r'^ponto/(?P<ponto>\d+)/linha/(?P<linha>\d+)/horarios/$',
        'previsoes', name='previsoes'),
)
# Registros
urlpatterns += patterns('apps.registros.views',
    url(r'^registro/', include('registros.urls', namespace='registro')),
)
# Media
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
