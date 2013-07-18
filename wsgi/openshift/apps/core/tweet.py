# -*- coding: UTF8 -*-
import time
import urllib
import random
import urllib2
import twitter
import cronjobs
from django.conf import settings
from django.http import HttpResponse, Http404
from django.utils.encoding import smart_str, smart_unicode
from time import strftime
from xml.dom.minidom import parse, parseString
from registros.models import Registros
from core.RepeatTimer import RepeatTimer

RAST_URL = 'http://rast.vitoria.es.gov.br/'

SADFACES = [u'☹', u'๏̯͡๏', u'».«', u'(͡๏̯͡๏)', u'(×̯×)', u'ಥ_ಥ', u'v_v',
            u'►_◄', u'►.◄', u'>.<', u'ಠ_ರೃ', u'ಠ╭╮ಠ', u'מּ_מּ', u'לּ_לּ',
            u'טּ_טּ', u'ಸ_ಸ', u'ಠ,ಥ', u'໖_໖', u'Ծ_Ծ', u'ಠ_ಠ', u'⇎_⇎',
            u'●_●', u'~̯~', u'◔̯◔', u'أ ̯ أ', u'(╥﹏╥)', u'(►.◄)',
            u'(ு८ு)', u'v(ಥ ̯ ಥ)v', u'ب_ب']


def uniq(alist):
    """
    Unico:
    Remove repeated records
    """
    set = {}
    return [set.setdefault(e, e) for e in alist if e not in set]


def addminutes(minutes):
    """
    De Minutos para HH:MM + hora atual:
    Recebe tempo em minutos, adiciona hora atual,
    transforma para o formato de hora e retorna
    """

    h = int(strftime("%H"))
    m = int(strftime("%M"))
    t = divmod(int(minutes) + m, 60)
    h = h + t[0]
    m = t[1]

    if h >= 24:
        t = divmod(h, 24)
        h = t[1]

    if m < 10:
        return str(h) + ':0' + str(m)
    elif h < 10:
        return '0' + str(h) + ':' + str(m)
    else:
        return str(h) + ':' + str(m)


def toHourMin(minutes):
    """
    De Minutos para HH:MM:
    Recebe tempo em minutos transforma para o formato de hora e retorna
    """
    t = divmod(int(minutes), 60)
    h = t[0]
    m = t[1]

    if h >= 24:
        t = divmod(h, 24)
        h = t[1]

    if h == 0:
        if m < 10:
            return ['', '0' + str(m)]
        else:
            return ['', str(m)]
    else:
        if m < 10:
            return [str(h), '0' + str(m)]
        elif h < 10:
            return ['0' + str(h), str(m)]
        else:
            return [str(h), str(m)]


def create_tweets(registros):
    """
    Cria Tweets:
    Recebe a hora atual (de 15 em 15 minutos) e retorna os tweets gerados
    """

    previsoes_xml = {}
    tweets = []

    # obtem previsoes
    for reg in registros:
        prev = previsao(reg)
        previsoes_xml.update({reg.ponto: prev})

    pontos = uniq(registros.values_list('ponto'))
    for ponto in pontos:
        linhas = uniq(registros.filter(ponto=ponto[0]).values_list('linha'))
        for linha in linhas:
            hs = horarios(previsoes_xml[ponto[0]], linha[0])
            tws = registros.filter(ponto=ponto[0], linha=linha[0])
            for tw in tws:
                tweets.append(tweet(tw.twitter, hs, linha[0]))

    # remove registros - somente esta vez
    #registros.filter(lembrar=0,falhou=False).delete()

    return tweets


def tweet(twitter_id, horarios, linha):
    """
    Constroi Tweet:
    Recebe o usuário e os horários estimados de chegada,
    monta e retorna o tweet
    """
    primeiro = ''
    mais_de_um = ''
    smile = ''
    toobad = ''
    prev = []
    # ordena os horarios
    horarios = sorted(horarios)
    if int(strftime("%S")) % 2:
        toobad = smart_str(random.choice(SADFACES))
        smile = '^-^'

    # Zero   
    if not horarios:
        return (
            '@{0} são {1} e seu ônibus ({2}) está sem previsão de chegada {3} '
            '#previsão').format(twitter_id, strftime("%H:%M"), linha, toobad)
    # negative one
    if horarios[0] == -1:
        return (
            '@{0} ocorreu um problema e não encontramos a #previsão do seu'
            ' ônibus ({1}) {2}. Tentaremos novamente em breve. {3}'
            ' #falhou').format(twitter_id, linha, toobad, smile)
    # previsao zero 
    if horarios[0] == 0:
        primeiro = (
            'são {0} seu ônibus ({1}) vai passar AGORA, vai pro ponto '
            'garotinho! {2} #previsão').format(strftime("%H:%M"), linha, smile)
        mais_de_um = (
            'AGORA, vai pro ponto garotinho! {0} o próximo').format(smile)
    else:
        if horarios[0] > 59:
            prev = toHourMin(horarios[0])
            primeiro = (
                'seu ônibus ({0}) vai passar daqui a {1}h e {2}min às {3} '
                '#previsão').format(
                    linha, prev[0], prev[1], addminutes(horarios[0]))
            mais_de_um = (
                'daqui a {0}h e {1}min às {2}').format(
                    prev[0], prev[1], addminutes(horarios[0]))
        else:
            primeiro = (
                'seu ônibus ({0}) vai passar daqui a {1} minutos às {2} '
                '#previsão').format(linha, horarios[0], addminutes(horarios[0]))
            mais_de_um = (
                'daqui a {0} minutos às {1}').format(
                    horarios[0], addminutes(horarios[0]))
    # Um
    if len(horarios) == 1:
        return '@' + str(twitter_id) + ' ' + primeiro
    # Um ou mais
    else:
        if horarios[1] > 59:
            prev = toHourMin(horarios[1])
            return (
                '@{0} seu ônibus ({1}) vai passar {2} e daqui a {3}h e {4}min '
                'às {5} #previsão').format(twitter_id, linha, mais_de_um,
                                    prev[0], prev[1],addminutes(horarios[1]))
        else:
            return (
                '@{0} seu ônibus ({1}) vai passar {2} e daqui a {3} minutos às'
                ' {4} #previsão').format(twitter_id, linha, mais_de_um,
                                        horarios[1], addminutes(horarios[1]))


@cronjobs.register
def resend_tweets():
    """
    Renvia Tweets
    """
    regs = []

    # get all regs failed
    regs = Registros.objects.filter(falhou=True).order_by('ponto')
    if not regs:
        return False

    tweets = create_tweets(regs)
    api = twitter.Api(consumer_key=settings.CONSUMER_KEY,
                    consumer_secret=settings.CONSUMER_SECRET,
                    access_token_key=settings.ACCESS_TOKEN_KEY,
                    access_token_secret=settings.ACCESS_TOKEN_SECRET)

    for tweet in tweets:
        api.PostUpdate(tweet)

    # set all regs to success
    regs.all().update(falhou=False)
    return True 


@cronjobs.register
def send_tweets():
    """
    Envia Tweets
    """
    regs = Registros.objects.none()

    h = int(strftime("%H"))
    m = int(strftime("%M"))
    # nao aceita registros repetidos
    regs = Registros.objects.filter(horas=h, minutos=m).order_by('ponto')
    if not regs:
        return False

    tweets = create_tweets(regs)

    api = twitter.Api(consumer_key=CONSUMER_KEY,
                    consumer_secret=CONSUMER_SECRET,
                    access_token_key=ACCESS_TOKEN_KEY,
                    access_token_secret=ACCESS_TOKEN_SECRET)

    for tweet in tweets:
        api.PostUpdate(tweet)

    return True


def previsao(registro):
    """
    Previsao:
    Envia ponto e linha para o servidor ponto-vitoria e retorna XML com
    previsão (a previsão contém todas linhas)
    """
    previsao = ''
    opener = urllib2.build_opener()
    opener.addheaders = [
        ('Referer', RAST_URL + 'pontovitoria/'),
        ('User-agent',
            'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.13 ' +
            '(KHTML, like Gecko) Chrome/9.0.597.98 Safari/534.13'),
        ('Accept', 'application/xml, text/xml, */*;q=0.5'),
        ('Accept-Language', 'pt-BR,pt;q=0.8,en-US;q=0.6,en;q=0.4'),
        ('Accept-Encoding', 'gzip,deflate,sdch'),
        ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'),
        ('Keep-Alive', 'timeout=15, max=94')
    ]

    try:
        urlopened = opener.open(
            RAST_URL + 'previsao-web-service/previsao.jsp?ponto=' +
            str(registro.ponto) + '&linha=' + str(registro.linha))
    except:
        registro.falhou = True
        registro.save()
        return None

    read = urlopened.read()
    urlopened.close()    
    return read


def horarios(ponto_xml, linha):
    """
    Horarios:
    Recebe XML do ponto e linha a ser consultada retorna previsões em minutos
    """

    if not ponto_xml:
        return [-1]  # Erro ao obter o XML da previsao

    horarios = []
    xml0 = parseString(ponto_xml)
    horarioAtual = xml0.childNodes[1].getElementsByTagName(
        "horarioAtual")[0].firstChild.data
    for estimativa in \
        xml0.childNodes[1].childNodes[1].getElementsByTagName("estimativa"):
        linha_id = estimativa.childNodes[3].childNodes[3].firstChild.data
        if linha_id == str(linha):
            linha_desc = estimativa.childNodes[3].childNodes[5].firstChild.data
            horarioEstimado = estimativa.childNodes[7].firstChild.data
            # extrai tempo de chegada e transforma para minutos
            horarios.append(
                (int(horarioEstimado) - int(horarioAtual)) / 60000)

    return horarios  # de chegada em minutos


def localizar(request, ref):
    """
    Localizar
    """
    data = urllib.urlencode({'referencia': smart_str(ref)})
    urlopen = urllib2.urlopen(
        RAST_URL + 'pontovitoria/utilidades/listaPontos?' + data)
    read = urlopen.read()
    urlopen.close()
    return HttpResponse(read)


def pontos(request):
    """
    Pontos
    """
    urlopen = urllib2.urlopen(
        RAST_URL + 'pontovitoria/utilidades/listaPontos/')
    read = urlopen.read()
    urlopen.close()
    return HttpResponse(read)


def linhas(request, ponto):
    """
    Linhas
    """
    urlopen = urllib2.urlopen(
        RAST_URL + 'pontovitoria/utilidades/listaLinhaPassamNoPonto/' +
                '?ponto_oid=' + str(ponto))
    read = urlopen.read()
    urlopen.close()
    return HttpResponse(read)


@cronjobs.register
def cria_registros():
    """
    Cria registros teste
    """
    horas = range(6, 24)
    minutos = [0, 15, 30, 45]
    linhas = ['071', '074', '1302', '1331', '1331PC', '171', '175', '302',
                '303', '310', '331', '332', '333']
    for h in horas:
        for m in minutos:
            r = Registros()
            r.twitter = 'morenocunha'
            r.ponto = 4045
            r.linha = random.choice(linhas)
            r.horas = h
            r.minutos = m
            r.lembrar = 0
            r.save()