#!/bin/sh
PROJECT_ROOT=/home/dotcloud/current
mkdir -p $PROJECT_ROOT/cron-logs
date >> $PROJECT_ROOT/cron-logs/cron_send_tweet.log 2>&1
/home/dotcloud/env/bin/python /home/dotcloud/current/manage.py cron send_tweets >> $PROJECT_ROOT/cron-logs/cron_send_tweet.log 2>&1
