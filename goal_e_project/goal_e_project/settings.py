"""
Django settings for goal_e_project project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

from dotenv import dotenv_values

# Environmental variables
CONFIG = dotenv_values('.env')
ENV = CONFIG.get('ENV')
USE_S3 = CONFIG.get('USE_S3') == 'true'

URL = CONFIG.get('URL')
URL_HTTPS = f'https://{URL}' if URL else None

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if ENV == 'prod':
    SECRET_KEY = CONFIG.get('SECRET_KEY')
else:
    SECRET_KEY = 'django-insecure-aah3zcz#e+iq$z3v=(zh^1s--dy2173)_0hmm1fdp)u0*exjt('


# SECURITY WARNING: don't run with debug turned on in production!

if ENV == 'prod':
    DEBUG = False

    CSRF_TRUSTED_ORIGINS = [URL_HTTPS]
    CORS_ORIGIN_WHITELIST = [URL_HTTPS]
else:
    DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', CONFIG.get('SERVER_IP'), URL]

# Application definition

INSTALLED_APPS = [
    'goal_e.apps.GoalEConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5',
    'fontawesomefree',
    'django_s3_storage'
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

ROOT_URLCONF = 'goal_e_project.urls'

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

WSGI_APPLICATION = 'goal_e_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if ENV == 'prod':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': CONFIG.get('DB_NAME'),
            'USER': CONFIG.get('DB_USER'),
            'PASSWORD': CONFIG.get('DB_PASS'),
            'HOST': CONFIG.get('DB_HOST'),
            'PORT': CONFIG.get('DB_PORT')
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

if USE_S3:
    STATICFILES_STORAGE = 'django_s3_storage.storage.StaticS3Storage'
    DEFAULT_FILE_STORAGE = 'django_s3_storage.storage.S3Storage'
    STATIC_URL = CONFIG.get('S3_URL')

    AWS_REGION = CONFIG.get('AWS_REGION')
    AWS_ACCESS_KEY_ID = CONFIG.get('S3_ACCESS')
    AWS_SECRET_ACCESS_KEY = CONFIG.get('S3_ACCESS_SECRET')

    AWS_S3_BUCKET_NAME = CONFIG.get('S3_NAME')
    AWS_S3_BUCKET_NAME_STATIC = CONFIG.get('S3_NAME')
else:
    STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Custom settings
LOGIN_URL = '/login'
