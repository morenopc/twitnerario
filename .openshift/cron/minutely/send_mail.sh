#!/bin/sh
source "$OPENSHIFT_HOMEDIR"python/virtenv/bin/activate
PROJECT_ROOT="$OPENSHIFT_HOMEDIR"app-root/repo/wsgi/openshift
python $PROJECT_ROOT/manage.py send_mail
