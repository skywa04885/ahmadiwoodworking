"""
Django settings for ahmadiwoodwork project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os.path
from pathlib import Path
from django.utils.translation import gettext_lazy as _

SECRET_KEY = 'django-insecure-m27779$j*^o-p&616)5+8z-_$mi86wt43lq&#k39@*$9_@iz4_'

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'app.db',
    }
}

ALLOWED_HOSTS = []

CONTACT_NOTIFICATION_TO_ADDRESSES = ['luke.rieff@gmail.com']
CONSULTATION_REQUEST_NOTIFICATION_TO_ADDRESSES = ['luke.rieff@gmail.com']

CKEDITOR_UPLOAD_PATH = "uploads/"

DEBUG = False

# Meta
META_SITE_PROTOCOL = 'https'
META_SITE_DOMAIN = 'ahmadiwoodwork.com'
META_SITE_NAME = 'Ahmadi Woodwork'
META_INCLUDE_KEYWORDS = [
    "woodcraft",
    "craftsmanship",
    "joinery",
    "wooden furniture",
    "interior design",
    "bespoke cabinets",
    "handcrafted",
    "Tehran woodworkers",
    "woodworking services",
    "home improvement",
    "custom woodwork",
    "woodworking projects",
    "fine woodworking",
    "cabinetmakers",
    "artisan",
    "woodshop",
    "woodworking tools",
    "Tehran craftsmen",
    "woodworking techniques",
    "wood species",
    "woodworking tips",
    "cabinet design",
    "furniture makers",
    "cabinet refinishing",
]

try:
    from .settings_local import *
except ImportError:
    pass

if not DEBUG:
    # Enables compression.
    COMPRESS_ENABLED = True
    COMPRESS_ROOT = STATIC_ROOT
    COMPRESS_OFFLINE = True
    COMPRESS_CSS_FILTERS = ["compressor.filters.cssmin.CSSMinFilter"]
    COMPRESS_JS_FILTERS = ["compressor.filters.jsmin.JSMinFilter"]
    COMPRESS_STORAGE = "compressor.storage.GzipCompressorFileStorage"
else:
    COMPRESS_ENABLED = False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    'meta',
    'rosetta',
    'website',
    'jazzmin',
    'ckeditor',
    'compressor',
    'cssmin',
    'jsmin',
    'ckeditor_uploader',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ahmadiwoodwork.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'ahmadiwoodwork.wsgi.application'

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

LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = (
    ('en', _('English')),
    ('fa', _('Persian')),
)

LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = 'tailwind'

STATICFILES_FINDERS = (  ##django compressor
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

# The URLs for the social media.
SOCIALS_BALE_URL = ''
SOCIALS_WHATSAPP_URL = ''

# The contact information.
PHONE_NUMBER = "+989122962718"
EMAIL = ""
