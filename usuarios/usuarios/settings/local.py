from .base import *
from django.apps import AppConfig


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret("DB_NAME"),
        'USER': get_secret("USER"),
        'PASSWORD': get_secret("PASSWORD"),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
#STATICFILES_DIRS = ["static"] # DECLARACION DE LA UBICACION DE LOS ARCHIVOS ESTATICOS
#STATIC_ROOT="staticfiles" #VER SI VA ASI O COMO, NO ESTOY SEGURO SI SE DECLARA ASI

# Lo de abajo es para que los archivos multimedia se guarden por defecto en la carpeta media, y que en la declaracion del "upload to" solo haya que poner la carpeta contenedora
MEDIA_URL = '/media/'
MEDIA_ROOT = "media"



# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# EMAIL SETTINGS
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = get_secret("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = get_secret("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587