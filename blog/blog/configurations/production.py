from .base import *        

DEBUG = False

#TODO: configurar el dominio al hacer deploy a production
ALLOWED_HOSTS = ['localhost','127.0.0.1' ,'midominio-production.com']

#TODO: configurar db para production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        #En caso de usar una postgres utilizo: 'ENGINE': 'django.db.backends.postgresql'
        #En caso de usar una mysql utilizo: 'ENGINE': 'django.db.backends.mysql'

        # 'NAME': os.getenv('DB_NAME'),

        # 'USER': os.getenv('DB_USER'),

        # 'PASSWORD': os.getenv('DB_PASSWORD'),

        # 'HOST': os.getenv('DB_HOST'),  # Por defecto localhost

        # 'PORT': os.getenv('DB_PORT'),  # Por defecto 3306 para MySQL
    }
}

os.environ['DJANGO_PORT'] = '8080'