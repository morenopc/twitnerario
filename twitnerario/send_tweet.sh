#!/bin/sh

PROJECT_ROOT=/home/moreno/projects/django/twitnerario

# activate virtual environment
#. $WORKON_HOME/pinax-dev/bin/activate

date >> $PROJECT_ROOT/logs/cron_send_tweet.log 2>&1
cd $PROJECT_ROOT
python manage.py cron send_tweets >> $PROJECT_ROOT/logs/cron_send_tweet.log 2>&1
