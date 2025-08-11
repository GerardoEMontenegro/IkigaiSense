from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

os.environ["DJANGO_PORT"] = "3000"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_PORT = 2525
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '61ed5ac48258fc'
EMAIL_HOST_PASSWORD = 'a3b2b168c2c786'
DEFAULT_FROM_EMAIL = 'webmaster@localhost'