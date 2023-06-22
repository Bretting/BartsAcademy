"""
Django settings for BartsAcademy project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str(os.environ.get('DEBUG')) == "1"

ENV_ALLOWED_HOST = os.environ.get('DJANGO_ALLOWED_HOST') or None
ALLOWED_HOSTS = ['127.0.0.1', '.ondigitalocean.app','.bartsacademy.nl','.bartsacademy.nl/']
if not DEBUG:
    ALLOWED_HOSTS += [os.environ.get('DJANGO_ALLOWED_HOST')]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #MyApps
    'Accounts',
    'Academy',

    #External apps
    'storages',
    'django_htmx',
    'tinymce',
    'django_cleanup.apps.CleanupConfig',
    'crispy_forms',
    'crispy_bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]

ROOT_URLCONF = 'BartsAcademy.urls'
LOGIN_URL = '/sign-in'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'BartsAcademy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")

POSTGRES_READY = (
    POSTGRES_DB is not None
    and POSTGRES_PASSWORD is not None
    and POSTGRES_USER is not None
    and POSTGRES_HOST is not None
    and POSTGRES_PORT is not None
)

if POSTGRES_READY:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": POSTGRES_DB,
            "USER": POSTGRES_USER,
            "PASSWORD": POSTGRES_PASSWORD,
            "HOST": POSTGRES_HOST,
            "PORT": POSTGRES_PORT,
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles-cdn" # in production, we want cdn

MEDIA_URL = "/media/"

if DEBUG:
    MEDIA_ROOT = BASE_DIR / 'media'
else:
    MEDIA_ROOT = BASE_DIR / "staticfiles-cdn" / "uploads"

if not DEBUG:
    from .cdn.conf import * # noqa

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# TinyMCE
TINYMCE_DEFAULT_CONFIG = {
'theme': "silver", # default value
'relative_urls': False, # default value
'paste_as_text': True,
'theme_advanced_buttons1': 'bold,italic,underline,bullist,numlist,link,unlink,styleselect,fontselect,fontsizeselect',
'width': '100%',
'height': 250,
'paste_text_sticky': True,
'paste_text_sticky_default': True,
'valid_styles': 'font-weight,font-style,text-decoration',
'fontsize_formats': "8pt 10pt 11pt 12pt 13pt 14pt 16pt 18pt 20pt 24pt 36pt",
'font_formats': 
    "Roboto=Roboto;" +
    "Roboto Serif=Roboto Serif;",
'content_style':"@import url('https://fonts.googleapis.com/css2?family=Roboto+Serif:ital@0;1&family=Roboto:ital@0;1&display=swap');"}
TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = False
TINYMCE_JS_URL = "https://cdn.tiny.cloud/1/i7tg69zsj8xu2h7jinf65cpdznto148y1qexevwopnv9m9ng/tinymce/6/tinymce.min.js?referrerpolicy=origin"


# Django-Resized

DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_QUALITY = 100
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'JPEG': ".jpg"}

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Geolocate API key

GEO_LOCATE_API = os.environ.get("GEO_LOCATE_API")