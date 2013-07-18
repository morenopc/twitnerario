from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

# Registros
urlpatterns = patterns('apps.registros.views',
    url(r'^$', 'pesquisar', name='pesquisar'),
    url(r'^registro/', include('registros.urls', namespace='registro')),
)
# Core Tweet
urlpatterns += patterns('apps.core.tweet',
    url(r'^localizar/(?P<ref>.+)/$', 'localizar', name='localizar'),
    url(r'^pontos/$', 'pontos', name='pontos'),
    url(r'^(?P<ponto>\d+)/linhas/$', 'linhas', name='linhas'),
    # includes
    url(r'^admin/', include(admin.site.urls)),
    # direct_to_template
    url(r'^facebookauth/$', direct_to_template,
        {'template': 'facebook_auth/facebook_auth.html'},
        name='facebook_auth'),
)
# TwitterAuth
urlpatterns += patterns('apps.twitterauth.views',
    url(r'^login/$', 'twitter_signin', name='login'),
    url(r'^return/$', 'twitter_return', name='return'),
)
# Media
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            { 'document_root': settings.MEDIA_ROOT }),
    )
