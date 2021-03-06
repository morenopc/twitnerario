#!/bin/bash
set -e
# variaveis
ADMIN_USER='admin'
ADMIN_PASSWORD='ad2&min3'
ADMIN_EMAIL='admin@twitnerario.net'
SITENAME="localhost:8000"
PYTHON="./venv/bin/python"
PROJECT_PATH="wsgi/openshift"
set -x
# virtualenv
if [ ! -d venv ]; then
    virtualenv --no-site-packages venv
fi
# requirements.txt
./venv/bin/pip install -r $PROJECT_PATH/requirements.txt
# DB(sqlite)
rm -f $PROJECT_PATH/dev.db
# syncdb and South --migrate
$PYTHON $PROJECT_PATH/manage.py syncdb --migrate --noinput
# admin account
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '$ADMIN_EMAIL', '$ADMIN_PASSWORD')" | $PYTHON $PROJECT_PATH/manage.py shell
# runserver
$PYTHON $PROJECT_PATH/manage.py runserver
