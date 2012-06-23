import djcelery
#from celery.schedules import crontab
import os, sys
from datetime import timedelta

PROJECT_DIR = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_DIR, 'apps'))

DEBUG=True
TEMPLATE_DEBUG=DEBUG
ADMINS=(('Moreno', 'moreno.pinheiro@gmail.com'),)
MANAGERS=ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_DIR, 'meuonibus.db'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Brazil
TIME_ZONE = 'America/Sao_Paulo'
LANGUAGE_CODE = 'pt-br'

SITE_ID = 1
USE_I18N = True
USE_L10N = True

# MEDIAS
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'

# STATIC
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '&k44voktmp5eao+fjulm*lyo)udj9m(gjt^o8*!7conibus'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'twitnerario.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    # me
    'registros',
    'oauth',
    'simplejson',
    'twitterauth',
    'form_utils',
    'core',
    'cronjobs',
    # heroku
    'djcelery',
    'djkombu',
)
# CELERY
djcelery.setup_loader()
BROKER_BACKEND = "djkombu.transport.DatabaseTransport"
CELERY_RESULT_DBURI = DATABASES['default']
#CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

#CELERYBEAT_SCHEDULE = {
#    # Execute every 15 minutes
#    "every-15-minutes": {
#        "task": "send_tweets",
#        #"schedule": crontab(minute="*/15"),
#        "schedule": crontab(minute="*/1"),
#        "args": (16, 16),
#    },
#}

# https://dev.twitter.com/apps/1331327/show
CONSUMER_KEY='GjDAsmaMQdZdli8pDXA'
CONSUMER_SECRET='lONZF93DzyXPB5974GxbUmqLxyvA9ZG3bXUoliYhG8'
ACCESS_TOKEN_KEY='397486100-T13Va0sXGROGkNpzLZBpZrZdvl2xycyJWpov4cWV'
ACCESS_TOKEN_SECRET='5F5ExGiDQM770mQKPTai3pAlq2A9ockVsK5oqtcwM'

AUTHENTICATION_BACKENDS = (
    #'backends.twitteroauth.TwitterBackend',
    'django.contrib.auth.backends.ModelBackend',
)
AUTH_PROFILE_MODULE = "twitterauth.UserProfile"

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
