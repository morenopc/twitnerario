#!/bin/sh
if [ $(($(date +%M) % 15)) -eq 0 ]; then
	LOGS_DIR="$OPENSHIFT_HOMEDIR"python-2.7/logs
	PROJECT_ROOT="$OPENSHIFT_HOMEDIR"python-2.7/repo/wsgi/openshift
	mkdir -p $LOGS_DIR/cron-logs
	date >> $LOGS_DIR/cron-logs/cron_send_tweet.log 2>&1
	"$OPENSHIFT_HOMEDIR"python-2.7/virtenv/bin/python $PROJECT_ROOT/manage.py cron send_tweets >> $LOGS_DIR/cron-logs/cron_send_tweet.log 2>&1
fi
