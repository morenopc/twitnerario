# -*- coding: UTF8 -*-

import cronjobs
from datetime import time, date, timedelta
from registros.models import Registros


@cronjobs.register
def apagar_tweets_enviados():
    """
        Somente uma vez:
        Apaga todos os tweets de anteontem e os de ontem que foram enviados
    """
    ontem = date.today() - timedelta(days=1)
    anteontem = ontem - timedelta(days=1)
    Registros.objects.filter(criado_em__contains=anteontem, lembrar=0).delete()
    tws = Registros.objects.filter(criado_em__contains=ontem,
                                    lembrar=0, falhou=False)
    for tw in tws:
        # se hora do registro for menor que a do agendamento
        if time(tw.criado_em.hour, tw.criado_em.minute) \
            < time(tw.horas, tw.minutos):
            tw.delete()

# semanais

# mensais

# anuais
