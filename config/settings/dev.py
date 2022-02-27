from .base import *
from django.core.exceptions import ImproperlyConfigured
import json

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
