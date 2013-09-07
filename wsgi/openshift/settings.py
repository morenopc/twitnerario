# -*- coding: utf-8 -*-
# Twitnerario django settings for openshift project.
from django.utils import simplejson
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
TEMPLATE_DEBUG = DEBUG

ADMINS = [('Admin', 'moreno.pinheiro@gmail.com')]
MANAGERS = ADMINS

if ON_OPENSHIFT:
    # os.environ['OPENSHIFT_MYSQL_DB_*'] variables can be used with databases created
    # with rhc cartridge add (see /README in this git repo)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'sqlite3.db'),
            'USER': '',
            'PASSWORD': '',
            'HOST': '', 
            'PORT': '',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(PROJECT_DIR, 'sqlite3.db'),
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

# Allow domain and subdomain
ALLOWED_HOSTS = ['*']

# Nose tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

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
    'django_nose',
    'cronjobs',
    'form_utils',
    'django_extensions',
    'templatetag_handlebars',
    'django_mailer',
)

# Nose tests
NOSE_ARGS = [
    '--with-notify',
    '--verbosity=2']

FIXTURE_DIRS = (os.path.join(PROJECT_DIR, 'fixtures'),)

# Twitter API
# https://dev.twitter.com/apps/1331327/show
TWITTER = simplejson.load(
    open(PROJECT_DIR + '/twitter_api.json'))
TWEET_MAX = 144
CONSUMER_KEY = TWITTER['CONSUMER_KEY']
CONSUMER_SECRET = TWITTER['CONSUMER_SECRET']
ACCESS_TOKEN_KEY = TWITTER['ACCESS_TOKEN_KEY']
ACCESS_TOKEN_SECRET = TWITTER['ACCESS_TOKEN_SECRET']

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

# Django-mailer
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'twitnerario@gmail.com'
EMAIL_HOST_PASSWORD = 'twit4nerario7'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# Django-mailer-2
EMAIL_BACKEND = 'django_mailer.smtp_queue.EmailBackend'
DEFAULT_FROM_EMAIL = 'twitnerario@gmail.com'

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
