# -*- coding:utf-8  -*-
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
import datetime
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "abkayit"))
COMMON_CONFIG_FILE='/home/ozge/abkayit.conf'
#COMMON_CONFIG_FILE='/opt/abkayit.config'
MEDIA_ROOT = "/home/ozge/web/abkayit/" #os.path.join(BASE_DIR, '/')
#MEDIA_ROOT = "/home/ozge/workspace/abkayit/abkayit" #os.path.join(BASE_DIR, '/')

MEDIA_URL = '/'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

EMAIL_FROM_ADDRESS="kayit@ab.org.tr"

from readconf import *
# SECURITY WARNING: keep the secret key used in production secret!
DJANGOSETTINGS=DjangoSettings()
SECRET_KEY = DJANGOSETTINGS.getsecretkey()
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

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
    'ckeditor_uploader',
    'django_countries',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
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
				os.path.join(BASE_DIR, 'locale/'),
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

LOGIN_URL="/"
USER_TYPES={"inst": "instructor", "stu": "student", "spe":"speaker", "par": "participant","hepsi":"hepsi"}

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
GENDER={'E':'Erkek', 'K':'Kadin','H':'Hepsi'}
UNIVERSITIES=[('Abant İzzet Baysal Üniversitesi (Bolu)','Abant İzzet Baysal Üniversitesi (Bolu)'),
    ('Adnan Menderes Üniversitesi (Aydın)','Adnan Menderes Üniversitesi (Aydın)'),
    ('Afyon Kocatepe Üniversitesi(Afyon)','Afyon Kocatepe Üniversitesi(Afyon)'),
    ('Akdeniz Üniversitesi (Antalya)','Akdeniz Üniversitesi (Antalya)'),
    ('Anadolu Üniversitesi (Eskişehir)','Anadolu Üniversitesi (Eskişehir)'),
    ('Ankara Üniversitesi(Ankara)','Ankara Üniversitesi(Ankara)'),
    ('Atatürk Üniversitesi (Erzurum)','Atatürk Üniversitesi (Erzurum)'),
    ('Atılım Üniversitesi (Ankara)','Atılım Üniversitesi (Ankara)'),
    ('Bahçeşehir Üniversitesi(İstanbul)','Bahçeşehir Üniversitesi(İstanbul)'),
    ('Balıkesir Üniversitesi(Balıkesir)','Balıkesir Üniversitesi(Balıkesir)'),
    ('Başkent Üniversitesi (Ankara)','Başkent Üniversitesi (Ankara)'),
    ('Beykent Üniversitesi (İstanbul)','Beykent Üniversitesi (İstanbul)'),
    ('Bilkent Üniversitesi (Ankara)','Bilkent Üniversitesi (Ankara)'),
    ('Boğaziçi Üniversitesi (İstanbul)','Boğaziçi Üniversitesi (İstanbul)'),
    ('Celâl Bayar Üniversitesi (Manisa)','Celâl Bayar Üniversitesi (Manisa)'),
    ('Cumhuriyet Üniversitesi (Sivas)','Cumhuriyet Üniversitesi (Sivas)'),
    ('Çağ Üniversitesi (Tarsus-İçel)','Çağ Üniversitesi (Tarsus-İçel)'),
    ('Çanakkale Onsekiz Mart Üniversitesi(Çanakkale)','Çanakkale Onsekiz Mart Üniversitesi(Çanakkale)'),
    ('Çankaya Üniversitesi (Ankara)','Çankaya Üniversitesi (Ankara)'),
    ('Çukurova Üniversitesi (Adana)','Çukurova Üniversitesi (Adana)'),
    ('Dicle Üniversitesi (Diyarbakır)','Dicle Üniversitesi (Diyarbakır)'),
    ('Doğuş Üniversitesi (İstanbul)','Doğuş Üniversitesi (İstanbul)'),
    ('Dokuz Eylül Üniversitesi (İzmir)','Dokuz Eylül Üniversitesi (İzmir)'),
    ('Dumlupınar Üniversitesi (Kütahya)','Dumlupınar Üniversitesi (Kütahya)'),
    ('Ege Üniversitesi (İzmir)','Ege Üniversitesi (İzmir)'),
    ('Erciyes Üniversitesi (Kayseri)','Erciyes Üniversitesi (Kayseri)'),
    ('Fatih Üniversitesi (İstanbul)','Fatih Üniversitesi (İstanbul)'),
    ('Fırat Üniversitesi (Elazığ)','Fırat Üniversitesi (Elazığ)'),
    ('Galatasaray Üniversitesi (İstanbul)','Galatasaray Üniversitesi (İstanbul)'),
    ('Gazi Üniversitesi (Ankara)','Gazi Üniversitesi (Ankara)'),
    ('Gaziantep Üniversitesi(Gaziantep)','Gaziantep Üniversitesi(Gaziantep)'),
    ('Gaziosmanpaşa Üniversitesi (Tokat)','Gaziosmanpaşa Üniversitesi (Tokat)'),
    ('Gebze Yüksek Teknoloji Enstitüsü(İzmit-Kocaeli)','Gebze Yüksek Teknoloji Enstitüsü(İzmit-Kocaeli)'),
    ('Hacettepe Üniversitesi (Ankara)','Hacettepe Üniversitesi (Ankara)'),
    ('Haliç Üniversitesi(İstanbul)','Haliç Üniversitesi(İstanbul)'),
    ('Harran Üniversitesi (Şanlıurfa)','Harran Üniversitesi (Şanlıurfa)'),
    ('Işık Üniversitesi (İstanbul)','Işık Üniversitesi (İstanbul)'),
    ('İnönü Üniversitesi (Malatya)','İnönü Üniversitesi (Malatya)'),
    ('İstanbul Üniversitesi(İstanbul)','İstanbul Üniversitesi(İstanbul)'),
    ('İstanbul Bilgi Üniversitesi(İstanbul)','İstanbul Bilgi Üniversitesi(İstanbul)'),
    ('İstanbul Kültür Üniversitesi(İstanbul)','İstanbul Kültür Üniversitesi(İstanbul)'),
    ('İstanbul Teknik Üniversitesi(İstanbul)','İstanbul Teknik Üniversitesi(İstanbul)'),
    ('İstanbul Ticaret Üniversitesi(İstanbul)','İstanbul Ticaret Üniversitesi(İstanbul)'),
    ('İzmir Yüksek Teknoloji Enstitüsü(İzmir)','İzmir Yüksek Teknoloji Enstitüsü(İzmir)'),
    ('İzmir Ekonomi Üniversitesi(İzmir)','İzmir Ekonomi Üniversitesi(İzmir)'),
    ('Kadir Has Üniversitesi(İstanbul)','Kadir Has Üniversitesi(İstanbul)'),
    ('Kafkas Üniversitesi (Kars)','Kafkas Üniversitesi (Kars)'),
    ('Kahramanmaraş Sütçü İmam Üniversitesi(Kahramanmaraş)','Kahramanmaraş Sütçü İmam Üniversitesi(Kahramanmaraş)'),
    ('Karadeniz Teknik Üniversitesi (Trabzon)','Karadeniz Teknik Üniversitesi (Trabzon)'),
    ('Kırıkkale Üniversitesi(Kırıkkale)','Kırıkkale Üniversitesi(Kırıkkale)'),
    ('Kocaeli Üniversitesi(Kocaeli-İzmit)','Kocaeli Üniversitesi(Kocaeli-İzmit)'),
    ('Koç Üniversitesi (İstanbul)','Koç Üniversitesi (İstanbul)'),
    ('Maltepe Üniversitesi (İstanbul)','Maltepe Üniversitesi (İstanbul)'),
    ('Marmara Üniversitesi (İstanbul)','Marmara Üniversitesi (İstanbul)'),
    ('Mersin Üniversitesi(Mersin-İçel)','Mersin Üniversitesi(Mersin-İçel)'),
    ('Mimar Sinan Üniversitesi (İstanbul)','Mimar Sinan Üniversitesi (İstanbul)'),
    ('Muğla Üniversitesi(Muğla)','Muğla Üniversitesi(Muğla)'),
    ('Mustafa Kemal Üniversitesi (Hatay)','Mustafa Kemal Üniversitesi (Hatay)'),
    ('Niğde Üniversitesi(Niğde)','Niğde Üniversitesi(Niğde)'),
    ('Okan Üniversitesi(İstanbul)','Okan Üniversitesi(İstanbul)'),
    ('Ondokuz Mayıs Üniversitesi (Samsun)','Ondokuz Mayıs Üniversitesi (Samsun)'),
    ('Orta Doğu Teknik Üniversitesi (Ankara)','Orta Doğu Teknik Üniversitesi (Ankara)'),
    ('Osmangazi Üniversitesi (Eskişehir)','Osmangazi Üniversitesi (Eskişehir)'),
    ('Pamukkale Üniversitesi (Denizli)','Pamukkale Üniversitesi (Denizli)'),
    ('Sabancı Üniversitesi(İstanbul)','Sabancı Üniversitesi(İstanbul)'),
    ('Sakarya Üniversitesi(Sakarya-Adapazarı)','Sakarya Üniversitesi(Sakarya-Adapazarı)'),
    ('Selçuk Üniversitesi (Konya)','Selçuk Üniversitesi (Konya)'),
    ('Süleyman Demirel Üniversitesi (Isparta)','Süleyman Demirel Üniversitesi (Isparta)'),
    ('Trakya Üniversitesi (Edirne)','Trakya Üniversitesi (Edirne)'),
    ('TOBB Ekonomi ve Teknoloji Üniversitesi(Ankara)','TOBB Ekonomi ve Teknoloji Üniversitesi(Ankara)'),
    ('Ufuk Üniversitesi (Ankara)','Ufuk Üniversitesi (Ankara)'),
    ('Uludağ Üniversitesi (Bursa)','Uludağ Üniversitesi (Bursa)'),
    ('Yaşar Üniversitesi (İzmir)','Yaşar Üniversitesi (İzmir)'),
    ('Yeditepe Üniversitesi (İstanbul)','Yeditepe Üniversitesi (İstanbul)'),
    ('Yıldız Teknik Üniversitesi (İstanbul)','Yıldız Teknik Üniversitesi (İstanbul)'),
    ('Yüzüncü Yıl Üniversitesi (Van)','Yüzüncü Yıl Üniversitesi (Van)'),
    ('Zonguldak Karaelmas Üniversitesi(Zonguldak)','Zonguldak Karaelmas Üniversitesi(Zonguldak)'),]
