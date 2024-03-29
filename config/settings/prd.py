import os
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

ALLOWED_HOSTS = ['knowledge-shared.com', 'www.knowledge-shared.com']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_USER'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'HOST': os.environ['DATABASE_HOST'],
        'PORT': '5432',
    }
}

# HTTPS Settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_SSL_REDIRECT = True

# Cloudinary config for user uploaded media
CLOUDINARY_STORAGE = {'CLOUD_NAME': os.environ['ClOUDINARY_CLOUD_NAME'],
                      'API_KEY': os.environ['ClOUDINARY_API_KEY'],
                      'API_SECRET': os.environ['ClOUDINARY_API_SECRET'], }

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ['EMAIL_HOST_USER']
DEFAULT_TO_EMAIL = os.environ['DEFAULT_TO_EMAIL']
SERVER_EMAIL = os.environ['EMAIL_HOST_USER']

ADMINS = [('Doug Mumme', 'dougmumme@gmail.com')]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'verbose': {
            '()': 'KnowledgeShare.utils.formatters.XMLLogFormatter'
        }
    },
    'handlers': {
        'file': {
            'level': os.environ['LOG_LEVEL'],
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'filename': 'logs/log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': os.environ['LOG_LEVEL'],
            'propagate': True,
        },
    },
}
