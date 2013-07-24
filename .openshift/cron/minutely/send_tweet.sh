#!/bin/sh
if [ $(($(date +%M) % 15)) -eq 0 ]; then
	source "$OPENSHIFT_HOMEDIR"python-2.7/activate_virtenv
	LOGS_DIR="$OPENSHIFT_HOMEDIR"python-2.7/logs
	PROJECT_ROOT="$OPENSHIFT_HOMEDIR"python-2.7/repo/wsgi/openshift
	mkdir -p $LOGS_DIR/cron-logs
	date >> $LOGS_DIR/cron-logs/cron_send_tweet.log 2>&1
	# python $PROJECT_ROOT/manage.py cron send_tweets >> $LOGS_DIR/cron-logs/cron_send_tweet.log 2>&1
	echo "from core import tweet; tweet.send_tweets()" | python $PROJECT_ROOT/manage.py shell >> $LOGS_DIR/cron-logs/cron_send_tweet.log 2>&1
fi
