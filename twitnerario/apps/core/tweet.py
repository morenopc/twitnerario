# -*- coding: UTF8 -*-

import twitter
import urllib2
import cronjobs
import time
from time import strftime
from xml.dom.minidom import parse, parseString
from django.utils.encoding import smart_str, smart_unicode
from django.http import HttpResponse
from registros.models import Registros
from core.RepeatTimer import RepeatTimer
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.task import task
from django.http import Http404

#
# Unico
#
def uniq(alist):
    """Remove repeated records"""
    set={}
    return [set.setdefault(e,e) for e in alist if e not in set]

#
# De Minutos para HH:MM + hora atual
#
def addminutes(minutes):
    """Recebe tempo em minutos, adiciona hora atual, transforma para o formato de hora e retorna"""
    h=int(strftime("%H"))
    m=int(strftime("%M"))
    t=divmod(int(minutes)+m,60)
    h=h+t[0]
    m=t[1]
    
    if h>=24:
        t=divmod(h,24)
        h=t[1]
    
    if m<10:
        return str(h)+':0'+str(m)
    elif h<10:
        return '0'+str(h)+':'+str(m)
    else:
        return str(h)+':'+str(m)

#
# Cria Tweets
#
def create_tweets(h,m):
    """Recebe a hora atual (de 15 em 15 minutos) e retorna os tweets gerados"""
    
    regs=[]
    previsoes_xml={}
    tweets=[]
    
    # nao aceita registros repetidos
    regs=Registros.objects.filter(horas=h, minutos=m).order_by('ponto')
    if not regs:
        return tweets
    
    # obtem previsoes
    for reg in regs:
        prev=previsao(reg.ponto,reg.linha)
        previsoes_xml.update({reg.ponto:prev})
    
    pontos=uniq(regs.values_list('ponto'))
    for ponto in pontos:
        linhas=uniq(regs.filter(ponto=ponto[0]).values_list('linha'))
        for linha in linhas:
            hs=horarios(previsoes_xml[ponto[0]],linha[0])
            tws=regs.filter(ponto=ponto[0],linha=linha[0])
            for tw in tws:
                tweets.append(tweet(tw.twitter,hs))
    
    # remove registros - somente esta vez
    regs.filter(lembrar=0).delete()
    
    return tweets

#
# Constroi Tweet
#
def tweet(twitter_id,horarios):
    """Recebe o usuário e os horários estimados de chegada, monta e retorna o tweet"""
    primeiro=''
    smile=''
    toobad=''
    # ordena os horarios
    horarios=sorted(horarios)
    if int(strftime("%S"))%2:
        toobad=' :/'
        smile=' ^-^'
        
    try:
        if horarios[0]==0:
            primeiro='agora, vai pro ponto garotinho! '+strftime("%H:%M:%S")+smile
        else:
            primeiro='daqui a '+str(horarios[0])+' minutos às '+addminutes(horarios[0])
    except:
        return '@'+str(twitter_id)+' seu ônibus está sem previsão de chegada '+strftime("%H:%M:%S")+toobad
    
    if len(horarios)>1:
        return '@'+str(twitter_id)+' seu ônibus vai passar '+primeiro+' e daqui a '+str(horarios[1])+' minutos às '+addminutes(horarios[1])
            
    else:
        return '@'+str(twitter_id)+' seu ônibus vai passar '+primeiro

#
# Envia Tweets
#
@cronjobs.register
def send_tweets():
    # (heroku) server time
    h=int(strftime("%H"))
    m=int(strftime("%M"))
    
    # minute :20 and :50 - end
    if m==20 or minute==50:
        return False
    # minute :10 and :40 - add 5 minutes delay
    elif minute==10 or minute==40:
        time.sleep(290)
    # minute :00 and :30 - ok
    else:
        pass
    
    h=int(strftime("%H"))
    m=int(strftime("%M"))   
    tweets=create_tweets(h,m)
    if not tweets:
        return False
    
    api=twitter.Api(consumer_key='GjDAsmaMQdZdli8pDXA',
                    consumer_secret='lONZF93DzyXPB5974GxbUmqLxyvA9ZG3bXUoliYhG8',
                    access_token_key='397486100-T13Va0sXGROGkNpzLZBpZrZdvl2xycyJWpov4cWV',
                    access_token_secret='5F5ExGiDQM770mQKPTai3pAlq2A9ockVsK5oqtcwM')
    
    for tweet in tweets:
        api.PostUpdate(tweet)
    
    return True

#
# Previsao
#
def previsao(ponto,linha):
    """Envia ponto e linha para o servidor ponto-vitoria e retorna XML com previsão (a previsão contém todas linhas)"""
    previsao=''
    opener = urllib2.build_opener()
    opener.addheaders = [
    ('Referer','http://rast.vitoria.es.gov.br/pontovitoria/'),
    ('User-agent', 'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.98 Safari/534.13'),
    ('Accept','application/xml, text/xml, */*;q=0.5'),
    ('Accept-Language','pt-BR,pt;q=0.8,en-US;q=0.6,en;q=0.4'),
    ('Accept-Encoding','gzip,deflate,sdch'),
    ('Accept-Charset','ISO-8859-1,utf-8;q=0.7,*;q=0.3'),
    ('Keep-Alive','timeout=15, max=94')]
    previsao=opener.open('http://rast.vitoria.es.gov.br/previsao-web-service/previsao.jsp?ponto='+str(ponto)+'&linha='+str(linha)+'')
    
    return previsao.read()
    
#
# Horarios
#
def horarios(ponto_xml,linha):
    """Recebe XML do ponto e linha a ser consultada retorna previsões em minutos"""
    horarios=[]
    xml0=parseString(ponto_xml)
    horarioAtual=xml0.childNodes[1].getElementsByTagName("horarioAtual")[0].firstChild.data
    for estimativa in xml0.childNodes[1].childNodes[1].getElementsByTagName("estimativa"):
        linha_id=estimativa.childNodes[3].childNodes[3].firstChild.data
        if linha_id == str(linha):
            linha_desc=estimativa.childNodes[3].childNodes[5].firstChild.data
            horarioEstimado=estimativa.childNodes[7].firstChild.data
            # extrai tempo de chegada e transforma para minutos
            horarios.append((int(horarioEstimado)-int(horarioAtual))/60000)
    
    return horarios # de chegada em minutos

#
# Pontos
#
def pontos(request):
    info=urllib2.urlopen('http://rast.vitoria.es.gov.br/pontovitoria/utilidades/listaPontos/')
    return HttpResponse(info.read())

#
# Linhas
#
def linhas(request, ponto):
    info=urllib2.urlopen('http://rast.vitoria.es.gov.br/pontovitoria/utilidades/listaLinhaPassamNoPonto/?ponto_oid='+str(ponto))
    return HttpResponse(info.read())
