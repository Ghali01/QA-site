"""
Django settings for interviewsquestions project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9=lqwkpp6g!ae@)35f365ffs*v5b%kvno4xrzzof&y1%37=zgo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '192.168.1.5',
    'localhost',
    '127.0.0.1',
    'interviewsquestions.com',
    'www.interviewsquestions.com',
]


# Application definition

INSTALLED_APPS = [

    'dashboard.apps.DashboardConfig',
    'authusers.apps.AuthusersConfig',
    'content.apps.ContentConfig',
    'moderators.apps.ModeratorsConfig',
    'profiles.apps.ProfilesConfig',
    'feedback.apps.FeedbackConfig',
    'polls.apps.PollsConfig',
    'misc.apps.MiscConfig',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'interviewsquestions.utilities.datetime.TimezoneMiddleware',
    'interviewsquestions.utilities.lastSeenMiddleware.lastSeenMiddleware',
    'interviewsquestions.utilities.langMiddleware.langMiddleware'
]

ROOT_URLCONF = 'interviewsquestions.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.joinpath('templates')],
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

WSGI_APPLICATION = 'interviewsquestions.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'interviewsdb',
        'USER':'postgres',
        'PASSWORD':'12345',
        'PORT':'5432'
    }
}


AUTHENTICATION_BACKENDS=['interviewsquestions.utilities.loginBackend.LoginByEmail']


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'moho.stmp@gmail.com'
EMAIL_HOST_PASSWORD = '1234qwER'
EMAIL_PORT = '587'
EMAIL_USE_TLS=True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT=BASE_DIR.joinpath('static')
STATICFILES_DIRS=[
    BASE_DIR.joinpath('interviewsquestions/static')
    ]
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL='/media/'
MEDIA_ROOT=BASE_DIR.joinpath('media')

import django.contrib.messages.constants as messages
MESSAGE_TAGS={
    messages.ERROR:'danger'
}
LOCALE_PATHS=[
    BASE_DIR.joinpath('locale'),
    ]