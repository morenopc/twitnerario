from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin
from twitterauth.views import twitter_signin, twitter_return
from core.tweet import pontos, linhas, send_tweets
admin.autodiscover()

urlpatterns=patterns('',
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$',include('registros.urls', namespace='registro')),
    url(r'^registro/', include('registros.urls', namespace='registro')),
    url('^login/$', twitter_signin, name='login'),
    url('^return/$', twitter_return, name='return'),
    url(r'^pontos/$', pontos, name='pontos'),
    url(r'^(\d+)/linhas/$', linhas, name='linhas'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT }),
    )
