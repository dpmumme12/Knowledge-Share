from django.core.exceptions import ImproperlyConfigured
import json
from .base import *

# JSON-based secrets module
with open('dev_env.json') as f:
    env_vars = json.load(f)

def get_env_var(var, env_vars=env_vars):
    '''Get the secret variable or return explicit exception.'''
    try:
        return env_vars[var]
    except KeyError:
        error_msg = f'Set the {var} environment variable'
    raise ImproperlyConfigured(error_msg)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_r%7wu1$(4_r0l-1zvcr#_ut1(u%s49t2)h6!%dbdbqnmqvbna'

ALLOWED_HOSTS = ['*']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env_var('Postgres_Database_NAME'),
        'USER': get_env_var('Postgres_USER'),
        'PASSWORD': get_env_var('Postgres_PASSWORD'),
        'HOST': get_env_var('Postgres_HOST'),
        'PORT': '5432',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

MEDIA_ROOT = APPS_DIR / 'media'
STATIC_URL = 'static/'


# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = get_env_var('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_var('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = get_env_var('EMAIL_HOST_USER')
DEFAULT_TO_EMAIL = get_env_var('DEFAULT_TO_EMAIL')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/logger.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
