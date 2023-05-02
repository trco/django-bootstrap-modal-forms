import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'ke2rim3a=ukld9cjh6$d$fb%ztgobvrs807i^d!_whg%@n^%v#'
DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap_modal_forms',
    'widget_tweaks',
    'examples',
    'tests',
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

ROOT_URLCONF = 'setup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
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

WSGI_APPLICATION = 'setup.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(Path(BASE_DIR, 'db.sqlite3')),
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# No password rules in development
AUTH_PASSWORD_VALIDATORS = []
# Simple (and unsecure) but fast password hasher in development
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

# No internationalization for this project
USE_I18N = False
USE_L10N = False
USE_TZ = False

STATICFILES_FINDERS = [
    # searches in STATICFILES_DIRS
    'django.contrib.staticfiles.finders.FileSystemFinder',
    # searches in STATIC subfolder of each app
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATIC_URL = '/static/'
