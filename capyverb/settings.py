"""
Django settings for capyverb project.
"""

import os
from pathlib import Path
import dj_database_url
import environ

env = environ.Env()


BASE_DIR = Path(__file__).resolve().parent.parent


DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

SECRET_KEY = os.environ.get('SECRET_KEY', 'chave-local-desenvolvimento')

ALLOWED_HOSTS = ['capyverb-github-io.onrender.com', 'localhost', '127.0.0.1', '.onrender.com','capyverbgithubio-production.up.railway.app','.railway.app',]


if 'DATABASE_URL' in os.environ:
    
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'princi',  
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'capyverb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, ''),
            os.path.join(BASE_DIR, 'princi/templates'),
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'capyverb.wsgi.application'

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


LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


if not DEBUG:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGINS = [
        'https://capyverb-github-io.onrender.com',
        'https://*.onrender.com',
        'https://capyverbgithubio-production.up.railway.app',
        'https://*.railway.app',
    ]
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True


if DEBUG:
    
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    print("🔧 MODO DESENVOLVIMENTO: Emails no console")
else:
    
    print("🚀 MODO PRODUÇÃO: Emails reais via Resend")
    

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'capyverb@outlook.com')
SITE_URL = os.environ.get('SITE_URL', 'https://capyverb-github-io.onrender.com')
