"""
Django settings for support_center project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8d6f!wh%(yazbwsk%cb$u!v1#ex)4jm2*7&zfh!5x3^=3-m&on'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '212.191.92.101']

# Email settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'redlicki.grzegorz@gmail.com'
EMAIL_HOST_PASSWORD = 'xjqhnmuwssvewnkz'


# Authentication settings

AUTH_USER_MODEL = "cti.User"

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'cti.backends.LDAPBackend',
)

LDAP_AUTH_URL = "ldap://10.105.10.97"
LDAP_AUTH_SEARCH_BASE = "dc=cti,dc=lan"
LDAP_AUTH_CONNECTION_USERNAME = "cn=nss,dc=cti,dc=lan"
LDAP_AUTH_CONNECTION_PASSWORD = "alamakota"


# Application definition

INSTALLED_APPS = [
    'cti.apps.CtiConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ldap3',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'support_center.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'cti/templates/cti/admin'),
            os.path.join(BASE_DIR, 'cti/templates/cti/client'),
            os.path.join(BASE_DIR, 'cti/templates/cti/scripts')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'support_center.wsgi.cti'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

deployment = True
migration = False

if deployment:
    if migration:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'sql7144346',
                'USER': 'sql7144346',
                'PASSWORD': 'gaTmKQXHxm',
                'HOST': 'sql7.freemysqlhosting.net',
                'PORT': '3306',
                'OPTIONS': {
                    'init_command': 'SET default_storage_engine=INNODB',
                }
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'sql7144346',
                'USER': 'sql7144346',
                'PASSWORD': 'gaTmKQXHxm',
                'HOST': 'sql7.freemysqlhosting.net',
                'PORT': '3306',
                'OPTIONS': {
                    'init_command': 'SET default_storage_engine=INNODB',
                }
            },
            'invbook': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'invbook',
                'USER': 'student',
                'PASSWORD': 'student',
                'HOST': '10.105.10.194',
                'PORT': '3306',
                'OPTIONS': {
                    'init_command': 'SET default_storage_engine=INNODB',
                }
            }
        }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'support_center_test_database',
            'USER': 'root',
            'PASSWORD': 'root',
            'HOST': 'localhost',
            'PORT': '3306',
            'OPTIONS': {
                'init_command': 'SET default_storage_engine=INNODB',
            }
        }
    }

INVBOOK_TABLES = ['b010t4', 'b010t6', 'b010t8', 'b011t4', 'b011t6', 'b011t8', 'b020']

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'pl'

LANGUAGES = [
    ('en', _('English')),
    ('pl', _('Polish')),
]

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
