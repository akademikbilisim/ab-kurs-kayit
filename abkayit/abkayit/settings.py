"""
Django settings for abkayit project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "abkayit"))
COMMON_CONFIG_FILE='/opt/abkayit.config'

MEDIA_ROOT = "/opt/ab-kurs-kayit/abkayit" #os.path.join(BASE_DIR, '/')
MEDIA_URL = '/'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

from readconf import *
# SECURITY WARNING: keep the secret key used in production secret!
DJANGOSETTINGS=DjangoSettings()
SECRET_KEY = DJANGOSETTINGS.getsecretkey()
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.views',
    'abkayit',
    'userprofile',
	'seminar',
	'training',
	'ckeditor',
	'django_countries',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
ROOT_URLCONF = 'abkayit.urls'

WSGI_APPLICATION = 'abkayit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DBCONF=DBconfig()

DATABASES = {
	'default': {
		'ENGINE'	: 'django.db.backends.postgresql_psycopg2',
		'NAME'		: DBCONF.getdatabase(),
		'USER'		: DBCONF.getdbuser(),
		'PASSWORD'	: DBCONF.getdbpass(),
		'HOST'		: DBCONF.getdbhost(),
		'PORT'		: DBCONF.getdbport()
    	}
}
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
LOCALE_PATHS = (
				os.path.join(BASE_DIR, '../locale'),
                '/usr/local/lib/python2.7/dist-packages/django_countries/locale/',
                )

LANGUAGE_CODE = 'tr'

#TIME_ZONE = 'GMT'
TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_L10N = True

USE_TZ = True
DATE_FORMAT = 'dMY'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
)
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates/'),
)

LOGIN_URL="/accounts/login"
USER_TYPES={"inst": "instructor", "stu": "student", "spe":"speaker", "par": "participant"}

CKEDITOR_UPLOAD_PATH = "/static/"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] [%(clientip)s - %(user)-8s] %(levelname)s [%(name)s:%(lineno)s]  %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + "/logfile",
            'maxBytes': 2097152,
            'backupCount': 200,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'abkayit': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
        },
        'userprofile': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
        },
        'seminar': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
        },
		'training': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
        },

    }
}
