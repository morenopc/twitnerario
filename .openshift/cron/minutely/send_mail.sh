#!/bin/sh
source "$OPENSHIFT_HOMEDIR"python-2.7/activate_virtenv
PROJECT_ROOT="$OPENSHIFT_HOMEDIR"python-2.7/repo/wsgi/openshift
python $PROJECT_ROOT/manage.py send_mail