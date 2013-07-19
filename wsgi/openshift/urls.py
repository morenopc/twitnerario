from django.conf.urls import url, include, patterns
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

# Registros
urlpatterns = patterns('apps.registros.views',
    url(r'^$', 'pesquisar', name='pesquisar'),
    url(r'^registro/', include('registros.urls', namespace='registro')),
)
# Core Tweet
urlpatterns += patterns(
    'apps.core.tweet',
    url(r'^localizar/(?P<ref>.+)/$', 'localizar', name='localizar'),
    url(r'^pontos/$', 'pontos', name='pontos'),
    url(r'^pontos/json$', 'pontos_json', name='pontos_json'),
    url(r'^(?P<ponto>\d+)/linhas/$', 'linhas', name='linhas'),
    # includes
    url(r'^admin/', include(admin.site.urls)),
    # direct_to_template
    url(r'^facebookauth/$', TemplateView.as_view(template_name='facebook_auth.html')),
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
