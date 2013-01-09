from celery.schedules import crontab
from celery.task import periodic_task

from core.tweet import send_tweets

import logging
logger = logging.getLogger(__name__)

# Every fifteen minutes
@periodic_task(run_every=crontab(minute='*/15'))
def every_fifteen_tasks():
    send_tweets()
    logger.debug("Sending tweets ... ")
