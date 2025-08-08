from .base import *

DEBUG = False
#TODO: configurar el dominio al hacer deplloy a production
ALLOWED_HOSTS = ["127.0.0.1","midominio-production.com"]

#TODO: configurar la base de datos para production

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',

        #En caso de usar postgresql, descomentar la siguiente línea y comentar la de sqlite3
        #'ENGINE': 'django.db.backends.postgresql',
        #En caso de usar mysql, descomentar la siguiente línea y comentar la de sqlite3
        # 'ENGINE': 'django.db.backends.mysql',
        #NAME: os.getenv('DB_NAME'),
        #USER: os.getenv('DB_USER'),
        #PASSWORD: os.getenv('DB_PASSWORD'),
        #HOST: os.getenv('DB_HOST'),
        #PORT: os.getenv('DB_PORT'),  # Por defecto PostgreSQL usa el puerto 5432
    }
}
os.environ["DJANGO_PORT"] = "8080"