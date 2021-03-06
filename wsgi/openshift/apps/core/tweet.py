# -*- coding: UTF8 -*-
import re
import random
import twitter
import logging
import cronjobs
import requests
from time import strftime
from django.conf import settings
from django.utils.encoding import smart_str
from xml.dom.minidom import parse, parseString
from registros.models import Registros
from apps.core.models import Configuracao
# logger
logger = logging.getLogger(__name__)

SADFACES = [u'☹', u'๏̯͡๏', u'».«', u'(͡๏̯͡๏)', u'(×̯×)', u'ಥ_ಥ', u'v_v',
            u'►_◄', u'►.◄', u'>.<', u'ಠ_ರೃ', u'ಠ╭╮ಠ', u'מּ_מּ', u'לּ_לּ',
            u'טּ_טּ', u'ಸ_ಸ', u'ಠ,ಥ', u'໖_໖', u'Ծ_Ծ', u'ಠ_ಠ', u'⇎_⇎',
            u'●_●', u'~̯~', u'◔̯◔', u'أ ̯ أ', u'(╥﹏╥)', u'(►.◄)',
            u'(ு८ு)', u'v(ಥ ̯ ಥ)v', u'ب_ب']


def previsao_key():
    """"""
    url = Configuracao.objects.get(descricao='default')
    resposta = requests.get(url.previsao_origin + url.previsao_js)
    return re.search(r'validar\|(\d+)\|success', resposta.content).group(1)


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


def connect_twitter_api():
    return twitter.Api(consumer_key=settings.CONSUMER_KEY,
                    consumer_secret=settings.CONSUMER_SECRET,
                    access_token_key=settings.ACCESS_TOKEN_KEY,
                    access_token_secret=settings.ACCESS_TOKEN_SECRET)


def create_tweets(registros):
    """
    Recebe a hora atual (de 15 em 15 minutos) e
    retorna lista de tweets criados
    """

    previsoes_xml = {}
    tweets = []
    # obtem chave de acesso
    key = previsao_key()

    # obtem previsoes
    for registro in registros:
        # função previsao(registro, key)
        prev = previsao(registro, key)
        previsoes_xml.update({registro.ponto: prev.content})

    pontos = uniq(registros.values_list('ponto'))
    for ponto in pontos:
        linhas = uniq(registros.filter(ponto=ponto[0]).values_list('linha'))
        for linha in linhas:
            # função horarios(ponto_xml, linha)
            hs = horarios(previsoes_xml[ponto[0]], linha[0])
            tws = registros.filter(ponto=ponto[0], linha=linha[0])
            for tw in tws:
                # função tweet(twitter_id, horarios, linha)
                tweets.append(tweet(tw.twitter, hs, linha[0]))

    return tweets


def tweet(twitter_id, horarios, linha):
    """
    Constroi Tweet:
    Recebe o usuário e os horários estimados de chegada,
    monta e retorna o tweet
    """

    primeiro = mais_de_um = ''
    smile = toobad = ''
    prev = []
    # ordena os horarios
    horarios = sorted(horarios)
    if int(strftime("%S")) % 2:
        toobad = smart_str(random.choice(SADFACES))
        smile = '^-^'

    # Zero
    if not horarios:
        tweet = (
            '@{0} são {1} e seu ônibus ({2}) está sem previsão de chegada {3} '
            '#previsão').format(twitter_id, strftime("%H:%M"), linha, toobad)

        if len(tweet) > settings.TWEET_MAX:
            return tweet[:settings.TWEET_MAX]
        return tweet

    # negative one
    elif horarios[0] == -1:
        tweet = (
            '@{0} ocorreu um problema e não encontramos a #previsão do seu'
            ' ônibus ({1}) {2}. Tentaremos novamente em breve. {3}'
            ' #falhou').format(twitter_id, linha, toobad, smile)
    # previsao zero
    elif horarios[0] == 0:
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
                '#previsão').format(
                    linha, horarios[0], addminutes(horarios[0]))
            mais_de_um = (
                'daqui a {0} minutos às {1}').format(
                    horarios[0], addminutes(horarios[0]))
    # Um
    if len(horarios) == 1:
        tweet = '@' + str(twitter_id) + ' ' + primeiro
    # Um ou mais
    else:
        if horarios[1] > 59:
            prev = toHourMin(horarios[1])
            tweet = (
                '@{0} seu ônibus ({1}) vai passar {2} e daqui a {3}h e {4}min '
                'às {5} #previsão').format(twitter_id, linha, mais_de_um,
                                    prev[0], prev[1], addminutes(horarios[1]))
        else:
            tweet = (
                '@{0} seu ônibus ({1}) vai passar {2} e daqui a {3} minutos às'
                ' {4} #previsão').format(twitter_id, linha, mais_de_um,
                                        horarios[1], addminutes(horarios[1]))

    if len(tweet) > settings.TWEET_MAX:
        return tweet[:settings.TWEET_MAX]
    return tweet


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
    api = connect_twitter_api()

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
    api = connect_twitter_api()

    for tweet in tweets:
        api.PostUpdate(tweet)

    return True


def previsao_xml(ponto, linha, key):
    """Previsao XML"""
    url = Configuracao.objects.get(descricao='default')
    headers = {
            'Referer': 'http://rast.vitoria.es.gov.br/pontovitoria/',
            'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64) '
                    'AppleWebKit/537.11 (KHTML, like Gecko) '
                    'Chrome/23.0.1271.95 Safari/537.11')
        }
    payload = {
        'ponto': ponto,
        'linha': linha,
        'key': key
    }
    return requests.get(
        url.previsao_origin + url.previsao_pathname,
        params=payload, headers=headers)


def previsao(registro, key):
    """
    Previsao:
    Envia ponto e linha para o servidor ponto-vitoria e retorna XML com
    previsão (a previsão contém todas linhas)
    """
    
    try:
        resposta = previsao_xml(registro.ponto, registro.linha, key)

    except Exception, e:
        registro.falhou = True
        registro.save()
        raise e

    return resposta


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
            horario = (int(horarioEstimado) - int(horarioAtual)) / 60000
            if horario > 0:
                horarios.append(horario)

    return horarios  # de chegada em minutos


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
