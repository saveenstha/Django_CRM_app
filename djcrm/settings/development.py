# myproject/settings/development.py

from .base import *

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", ".vercel.app", ".now.sh"]

# Local database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

# Development email backend
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
