"""
Django settings for snailshell_cp project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import logging

import environ

env = environ.Env()
BASE_DIR = environ.Path(__file__) - 2

CONTROL_PANEL_PORT = env.int('CONTROL_PANEL_PORT')
CONTROL_PANEL_ADMIN_USER = env.str('CONTROL_PANEL_ADMIN_USER')
CONTROL_PANEL_ADMIN_PASSWORD = env.str('CONTROL_PANEL_ADMIN_PASSWORD')
CONTROL_PANEL_CONTAINER_NAME = env.str('CONTROL_PANEL_CONTAINER_NAME')
CONTROL_PANEL_IMAGE_NAME = env.str('CONTROL_PANEL_IMAGE_NAME')
CONTROL_PANEL_IMAGE_TAG = env.str('CONTROL_PANEL_IMAGE_TAG')
CONTROL_PANEL_LINUX_USER = env.str('CONTROL_PANEL_LINUX_USER')

PORTAINER_ADMIN_USER = env.str('PORTAINER_ADMIN_USER')
PORTAINER_ADMIN_PASSWORD = env.str('PORTAINER_ADMIN_PASSWORD')
PORTAINER_BASE_URL = env.str('PORTAINER_BASE_URL')
PORTAINER_PORT = env.int('PORTAINER_PORT')
PORTAINER_INTERNAL_URL = env.str('PORTAINER_INTERNAL_URL')
PORTAINER_EXTERNAL_URL = env.str('PORTAINER_EXTERNAL_URL')
PORTAINER_LOCAL_ENDPOINT_ID = env.int('PORTAINER_LOCAL_ENDPOINT_ID')
PORTAINER_LOCAL_ENDPOINT_NAME = env.str('PORTAINER_LOCAL_ENDPOINT_NAME')
PORTAINER_DOCKER_CONTAINER_NAME = env.str('PORTAINER_DOCKER_CONTAINER_NAME')
PORTAINER_IMAGE_NAME = env.str('PORTAINER_IMAGE_NAME')
PORTAINER_IMAGE_TAG = env.str('PORTAINER_IMAGE_TAG')

PERSISTENT_DIR = env.str('PERSISTENT_DIR', '/data')
LOG_LEVEL = env.str('LOG_LEVEL', 'INFO')
STATIC_ROOT = env.str('STATIC_ROOT')

POSTGRES_USER = env.str('POSTGRES_USER')
POSTGRES_PASSWORD = env.str('POSTGRES_PASSWORD')
POSTGRES_DB = env.str('POSTGRES_DB')
POSTGRES_PORT = env.int('POSTGRES_PORT')
POSTGRES_IMAGE_NAME = env.str('POSTGRES_IMAGE_NAME')
POSTGRES_IMAGE_TAG = env.str('POSTGRES_IMAGE_TAG')
POSTGRES_CONTAINER_NAME = env.str('POSTGRES_CONTAINER_NAME')
POSTGRES_DBNAME_CONTROL_PANEL = env.str('POSTGRES_DBNAME_CONTROL_PANEL')


RABBITMQ_USER = env.str('RABBITMQ_USER')
RABBITMQ_PASSWORD = env.str('RABBITMQ_PASSWORD')
RABBITMQ_PORT = env.int('RABBITMQ_PORT')
RABBITMQ_MANAGEMENT_PORT = env.int('RABBITMQ_MANAGEMENT_PORT')
RABBITMQ_IMAGE_NAME = env.str('RABBITMQ_IMAGE_NAME')
RABBITMQ_IMAGE_TAG = env.str('RABBITMQ_IMAGE_TAG')
RABBITMQ_CONTAINER_NAME = env.str('RABBITMQ_CONTAINER_NAME')


MASTER_HOST = env.str('MASTER_HOST')
DOCKERD_API_PORT = env.int('DOCKERD_API_PORT')
DOCKER_LOCAL_SOCKET_PATH = env.str('DOCKER_LOCAL_SOCKET_PATH')

SECRET_KEY = env.str('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = ['*']
CMD_UNINSTALL_DOCKER = env.str('CMD_UNINSTALL_DOCKER')
CMD_INSTALL_DOCKER = env.str('CMD_INSTALL_DOCKER')
CMD_DOCKER_EXTERNAL_IP = env.str('CMD_DOCKER_EXTERNAL_IP')
CMD_DOCKER_RESTART = env.str('CMD_DOCKER_RESTART')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'snailshell_cp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'snailshell_cp.urls'

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

WSGI_APPLICATION = 'snailshell_cp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': POSTGRES_DB,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': MASTER_HOST,
        'PORT': POSTGRES_PORT,
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s %(levelname)s %(message)s',
)
