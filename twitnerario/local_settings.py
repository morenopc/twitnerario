from settings import *

PROJECT_DIR = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_DIR, 'apps'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'meuonibus.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}