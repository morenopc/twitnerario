# -*- coding: utf-8 -*-
# Twitnerario django settings for openshift project.
import imp, os, sys

# a setting to determine whether we are running on OpenShift
ON_OPENSHIFT = False
if os.environ.has_key('OPENSHIFT_REPO_DIR'):
    ON_OPENSHIFT = True

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(PROJECT_DIR, 'apps'))
if ON_OPENSHIFT:
    DEBUG = False
else:
    DEBUG = True
TEMPLATE_DEBUG = DEBUG = True

ADMINS = [('Admin', 'admin@twitnerario.net')]
MANAGERS = ADMINS

if ON_OPENSHIFT:
    # os.environ['OPENSHIFT_MYSQL_DB_*'] variables can be used with databases created
    # with rhc cartridge add (see /README in this git repo)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'sqlite3.db'),  # Or path to database file if using sqlite3.
            'USER': '',                      # Not used with sqlite3.
            'PASSWORD': '',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': os.path.join(PROJECT_DIR, 'sqlite3.db'),  # Or path to database file if using sqlite3.
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

# STATIC
STATIC_ROOT = os.path.join(PROJECT_DIR, '..', 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    # os.path.join(PROJECT_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make a dictionary of default keys
default_keys = { 'SECRET_KEY': 'vm4rl5*ymb@2&d_(gc$gb-^twq9w(u69hi--%$5xrh!xk(t%hw' }

# Replace default keys with dynamic values if we are in OpenShift
use_keys = default_keys
if ON_OPENSHIFT:
    imp.find_module('openshiftlibs')
    import openshiftlibs
    use_keys = openshiftlibs.openshift_secure(default_keys)

# Make this unique, and don't share it with anybody.
SECRET_KEY = use_keys['SECRET_KEY']

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
ALLOWED_HOSTS = [
    '*', # Allow domain and subdomains
]
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
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
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

###############################################################################
# Import local settings (override)
###############################################################################
try:
    from local_settings import *
except ImportError:
    pass
