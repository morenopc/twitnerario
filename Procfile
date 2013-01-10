web: python twitnerario/manage.py runserver 0.0.0.0:$PORT --noreload
worker: python twitnerario/manage.py celeryd -B -E -l info -c 2 --settings=settings
