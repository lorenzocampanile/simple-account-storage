"""
Django settings for simpleaccountstorage project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import configparser
from pathlib import Path
from django.urls import resolve


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Where the configuration file is stored
CONFIG_FILENAME = BASE_DIR / 'simpleaccountstorage.conf'
config_parser = configparser.ConfigParser()
config_parser.read(CONFIG_FILENAME)
config = config_parser['baseconfig']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['SECRET_KEY']

# Salt used for the encrypt/decrypt key
ENCRYPTION_KEY_SALT = config['ENCRYPTION_KEY_SALT']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.getboolean('DEBUG')

ALLOWED_HOSTS = config['ALLOWED_HOSTS'].split(',')

SESSION_COOKIE_SECURE = not DEBUG

CSRF_COOKIE_SECURE = not DEBUG

# CSRF Trused Origins
# https://docs.djangoproject.com/en/4.0/ref/settings/#csrf-trusted-origins

CSRF_TRUSTED_ORIGINS = config['CSRF_TRUSTED_ORIGINS'].split(',')


# CSRF Cookie domain
# https://docs.djangoproject.com/en/5.0/ref/settings/#csrf-cookie-domain

CSRF_COOKIE_DOMAIN = config.get('CSRF_COOKIE_DOMAIN')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party apps
    'rest_framework',
    'corsheaders',
    'rest_registration',

    # Project apps
    'authentication.apps.AuthenticationConfig',
    'accountstorage.apps.AccountstorageConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'simpleaccountstorage.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['simpleaccountstorage/templates/', BASE_DIR / "web-client/dist/"],
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


# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATICFILES_DIRS = [
    BASE_DIR / 'web-client/dist/',
]
STATIC_ROOT = BASE_DIR / 'static-root/'


WSGI_APPLICATION = 'simpleaccountstorage.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Custom user model
# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#substituting-a-custom-user-model

AUTH_USER_MODEL = "authentication.User"


# The URL where the user is redirected after the lohin
LOGIN_REDIRECT_URL = '/accounts/'


# The URL of the login page
LOGIN_URL = '/auth/login/'


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

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Django REST Framework settings
# https://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# Django REST Registration settings
# https://django-rest-registration.readthedocs.io/en/latest/quickstart.html

REST_REGISTRATION = {
    # Disable the reset password endpoint
    'RESET_PASSWORD_VERIFICATION_ENABLED': False,

    'REGISTER_VERIFICATION_URL': f"{config['FRONTEND_BASE_URL']}/verify-user",
    'REGISTER_EMAIL_VERIFICATION_URL': f"{config['FRONTEND_BASE_URL']}/verify-email/",

    'VERIFICATION_FROM_EMAIL': config.get('VERIFICATION_FROM_EMAIL', 'no-reply@example.com'),

    'REGISTER_VERIFICATION_EMAIL_TEMPLATES': {
        'subject': 'registration/registration-subject.txt',
        'body': 'registration/registration-message.txt',
    },
}


# Email configuration
# https://docs.djangoproject.com/en/4.2/topics/email/

EMAIL_HOST = config.get('EMAIL_HOST')
EMAIL_PORT = config.get('EMAIL_PORT')
EMAIL_HOST_USER = config.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config.get('EMAIL_USE_TLS')
EMAIL_TIMEOUT = config.get('EMAIL_TIMEOUT')
EMAIL_FROM = config.get('EMAIL_FROM')
SERVER_EMAIL = config.get('SERVER_EMAIL')

# Email this users when there is a 500 error
# https://docs.djangoproject.com/en/4.2/ref/settings/#admins

ADMINS = list(map(lambda x: ('', x), config.get('ADMINS', '').split(',')))


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': config.get('LOG_FILENAME', '/var/log/simple-account-storage/error.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG',
        },
        'owngrid': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}


# DEBUG configuration
if DEBUG:
    # Django CORS headers allowed origins
    # https://pypi.org/project/django-cors-headers/
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOWED_ORIGINS = [
        'http://127.0.0.1:5173',
    ]
    CORS_ALLOW_HEADERS = (
        "accept",
        "authorization",
        "content-type",
        "user-agent",
        "x-csrftoken",
        "x-requested-with",
        "x-encryption-key",
    )

    # Use Mailhog
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = '127.0.0.1'
    EMAIL_PORT = 1025
