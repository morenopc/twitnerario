from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings
from django.contrib import admin
#from twitterauth.views import twitter_signin, twitter_return
#from core.tweet import localizar, pontos, linhas, send_tweets
#from registros.views import pesquisar
admin.autodiscover()

# Registros
urlpatterns = patterns('registros.views',
    url(r'^$', 'pesquisar', name='pesquisar'),
    url(r'^registro/', include('registros.urls', namespace='registro')),
)
# Core Tweet
urlpatterns += patterns('core.tweet',
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
urlpatterns += patterns('twitterauth.views',
    url(r'^login/$', 'twitter_signin', name='login'),
    url(r'^return/$', 'twitter_return', name='return'),
)
# Media
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            { 'document_root': settings.MEDIA_ROOT }),
    )
