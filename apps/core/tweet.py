# -*- coding: UTF8 -*-

import twitter
import urllib2
from xml.dom.minidom import parse, parseString
from django.utils.encoding import smart_str, smart_unicode
from django.http import HttpResponse
from registros.models import Registros
from time import strftime
import cronjobs

#
# Unico
#
def uniq(alist):
    set = {}
    return [set.setdefault(e,e) for e in alist if e not in set]

#
# De Minutos para HH:MM
def addminutes(minutes):
    h=int(strftime("%H"))
    m=int(strftime("%M"))
    t=divmod(int(minutes)+m,60)
    h=h+t[0]
    m=t[1]
    
    if h>=24:
        t=divmod(h,24)
        h=t[0]
    
    if m<=10:
        return str(h)+':0'+str(m)
    else:
        return str(h)+':'+str(m)
    
#
# Cria Tweets
#
def create_tweets(h,m):
    """Recebe a hora atual (de 15 em 15 minutos) e retorna os tweets marcados para daqui a 30 minutos"""
   
    if m>=30:
        m-=30
        h+=1
    else:
        m+=30  
    
    regs=Registros.objects.filter(horas=h, minutos=m).order_by('ponto')
    previsoes_xml={}
    pnt=''
    for reg in regs:
        if pnt != reg.ponto:
            prev=previsao(reg.ponto,reg.linha)
            previsoes_xml.update({reg.ponto:prev})
        pnt=reg.ponto
    
    tweet=[]
    pontos=uniq(regs.values_list('ponto'))
    for ponto in pontos:
        linhas=uniq(regs.filter(ponto=ponto[0]).values_list('linha'))
        for linha in linhas:
            hs=horarios(previsoes_xml[ponto[0]],linha[0])
            tws=regs.filter(ponto=ponto[0],linha=linha[0])
            for tw in tws:
                tweet.append(tweets(tw.twitter,hs))
    
    return tweet

#
# Constroi Tweets
#
def tweets(twitter,horario):
    
    if len(horario)>1:
        ultimo=horario.pop()
        penultimo=horario.pop()
        tms=''
        for h in horario:
            tms+=addminutes(h)+', '
        
        return str(twitter)+' seus próximos ônibus irão passar às '+tms+addminutes(penultimo)+' e '+addminutes(ultimo)
            
    elif len(horario)==1:
        return str(twitter)+' seu próximo ônibus irá passar às '+addminutes(horario[0])
    
    return str(twitter)+' seu ônibus está sem previsão de chegada'

#
# Envia Tweets
#
@cronjobs.register
def send_tweets():
    h=int(strftime("%H"))
    m=int(strftime("%M"))
    tweets=create_tweets(h,m)
    api=twitter.Api(consumer_key='GjDAsmaMQdZdli8pDXA',consumer_secret='lONZF93DzyXPB5974GxbUmqLxyvA9ZG3bXUoliYhG8', access_token_key='397486100-T13Va0sXGROGkNpzLZBpZrZdvl2xycyJWpov4cWV',access_token_secret='5F5ExGiDQM770mQKPTai3pAlq2A9ockVsK5oqtcwM')
    for tweet in tweets:
        api.PostUpdate(str(h)+':'+str(m)+' '+tweet)

#
# Previsao
#
def previsao(ponto,linha):
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
def horarios(xml,linha):
    horarios=[]
    xml0=parseString(xml)
    for estimativa in xml0.childNodes[1].childNodes[1].getElementsByTagName("estimativa"):
        linha_id=estimativa.childNodes[3].childNodes[3].firstChild.data
        if linha_id == str(linha):
            linha_desc=estimativa.childNodes[3].childNodes[5].firstChild.data
            horarioEstimado=estimativa.childNodes[7].firstChild.data
            horarioPacote=estimativa.childNodes[9].firstChild.data
            horarios.append((int(horarioEstimado)-int(horarioPacote))/60000)
    
    return horarios

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
