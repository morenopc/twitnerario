import cronjobs
from core.tweet import send_tweets
from core.apaga_tweets import apagar_tweets_enviados


@cronjobs.register
def periodic_task():
    pass
