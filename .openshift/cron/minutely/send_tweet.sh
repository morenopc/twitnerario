#!/bin/sh
LOGS_DIR="$OPENSHIFT_HOMEDIR"python-2.6/logs
PROJECT_ROOT="$OPENSHIFT_HOMEDIR"python-2.6/repo/wsgi/openshift
mkdir -p $LOGS_DIR/cron-logs
date >> $LOGS_DIR/cron-logs/cron_send_tweet.log 2>&1
"$OPENSHIFT_HOMEDIR"python-2.6/virtenv/bin/python $PROJECT_ROOT/manage.py cron send_tweets >> $LOGS_DIR/cron-logs/cron_send_tweet.log 2>&1
