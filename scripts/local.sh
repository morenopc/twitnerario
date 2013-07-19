#!/bin/bash
set -e
# variaveis
ADMIN_USER='admin'
ADMIN_PASSWORD='ad2&min3'
ADMIN_EMAIL='moreno.pinheiro@gmail.com'
SITENAME="localhost:8000"
PYTHON="./venv/bin/python"
PROJECT="twitnerario"
set -x
# virtualenv
if [ ! -d venv ]; then
    virtualenv --no-site-packages venv
fi
# requirements.txt
./venv/bin/pip install -r $PROJECT/requirements.txt
# DB(sqlite)
rm -f dev.db
# syncdb and South --migrate
$PYTHON $PROJECT/manage.py syncdb --migrate --noinput
# admin account
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '$ADMIN_EMAIL', '$ADMIN_PASSWORD')" | $PYTHON $PROJECT/manage.py shell
# runserver
$PYTHON $PROJECT/manage.py runserver
