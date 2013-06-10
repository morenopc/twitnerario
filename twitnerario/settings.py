import json
import os, sys
from datetime import timedelta

PROJECT_DIR = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_DIR, 'apps'))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = [('Moreno', 'moreno.pinheiro@gmail.com')]
MANAGERS = ADMINS

try:
    f = open('/home/dotcloud/environment.json')
    DOTCLOUD = json.load(f)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'twitnerario',
            'USER': DOTCLOUD['DOTCLOUD_DATA_MYSQL_LOGIN'],
            'PASSWORD': DOTCLOUD['DOTCLOUD_DATA_MYSQL_PASSWORD'],
            'HOST': DOTCLOUD['DOTCLOUD_DATA_MYSQL_HOST'],
            'PORT': DOTCLOUD['DOTCLOUD_DATA_MYSQL_PORT'],
        }
    }
except IOError:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(PROJECT_DIR, 'dev.db'),
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
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
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static-files'),
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

ROOT_URLCONF = 'urls'

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
    'core',
    'registros',
    # apps
    'south',
    'cronjobs',
    'form_utils',
    'twitterauth',
    'django_extensions',
    'templatetag_handlebars',
)

# Twitter
# https://dev.twitter.com/apps/1331327/show
CONSUMER_KEY = 'GjDAsmaMQdZdli8pDXA'
CONSUMER_SECRET = 'lONZF93DzyXPB5974GxbUmqLxyvA9ZG3bXUoliYhG8'
ACCESS_TOKEN_KEY = '397486100-T13Va0sXGROGkNpzLZBpZrZdvl2xycyJWpov4cWV'
ACCESS_TOKEN_SECRET = '5F5ExGiDQM770mQKPTai3pAlq2A9ockVsK5oqtcwM'

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
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': '/var/log/supervisor/twitnerario.log',
            'maxBytes': 1024*1024*25, # 25 MB
            'backupCount': 5,
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
        # Catch All Logger -- Captures any other logging
        '': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}

###############################################################################
# Import local settings (override)
###############################################################################
try:
    from local_settings import *
except ImportError:
    pass
