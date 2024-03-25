import os
from pathlib import Path
import pymysql
from app.utils import (
  get_env,
  bool_from_str
)
import logging



pymysql.install_as_MySQLdb()
logging.getLogger('spectacular').setLevel(logging.ERROR)


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-lwhqj2z!w5^btau7n0e*33dv2gc1++9t5k8=bxx4ewir+#+*2k'

DEBUG = True

ALLOWED_HOSTS = get_env('ALLOWED_HOSTS', '*').split(',')

# cors
CORS_ALLOWED_ORIGINS = '*'
CORS_ORIGIN_WHITELIST = '*'
CORS_ALLOW_ALL_ORIGINS = True
# print(Users.objects.all())

# Application definition
BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = [
    'app'
]

THIRD_APPS = [
    'rest_framework',
    'simple_history',
    'rest_framework.authtoken',
    'drf_spectacular',
]

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_APPS


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware'
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'



print(get_env('DB_NAME',
        ))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_env(
            'DB_NAME',
            'test'
        ),
        'USER': get_env(
            'DB_USER',
            'root'
        ),
        'PASSWORD': get_env(
            'DB_PASSWORD',
            ''
        ),
        'HOST': get_env(
            'DB_HOST',
            'localhost'
        ),
        'PORT': get_env(
            'DB_PORT',
            '3306'
        ),
}}


AUTH_USER_MODEL = 'app.Users'


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

# idioma predeterminado de la aplicación
LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Caracas'

# internacionalización
USE_I18N = True

# localización
USE_L10N = True


USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'translate'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DATE_FORMAT': '%Y-%m-%d',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',  # noqa: E501
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'app.permissions.custom.TokenAuthGsoft',
    ),
    'PAGE_SIZE': 10,
    'MAX_PAGE_SIZE': 10
}

# swagger
SPECTACULAR_SETTINGS = {
    'TITLE': 'Payment Company System Documentation',  # Rename
    'DESCRIPTION': 'Retail System API',  # Rename
    'VERSION': get_env('VERSION', '1.0.0'),
    'SERVE_INCLUDE_SCHEMA': False,
    'SERVE_PUBLIC': True,
    'COMPONENT_SPLIT_REQUEST': True,
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        'supportedSubmitMethods': ['get', 'post', 'put', 'delete', 'patch'],
        'showRequestHeaders': True,
        'showOperationIds': True,
        'showCommonExtensions': True,
        'displayOperationId': True,
    },
}


# celery
# __all__ = ('celery_app',)
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TIMEZONE = "America/Caracas"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60