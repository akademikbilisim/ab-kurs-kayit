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

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "abkayit"))

'''
    COMMON_CONFIG_FILE: Veri tabani ayarlari ve secret key bu dosyada yer alir.
'''
COMMON_CONFIG_FILE = '/opt/kampyazilim.conf'

'''
    EMAIL_FROM_ADDRESS: Sistemden gonderilecek maillerin from adresi
'''
EMAIL_FROM_ADDRESS = "kamp@linux.org.tr"
EMAIL_HOST = "postaci.linux.org.tr"
EMAIL_PORT = 25

SEND_REPORT = True
REPORT_RECIPIENT_LIST = ["kamp-gelismeler@linux.org.tr"]
'''
    PREFERENCE_LIMIT: Kurs tercih limiti
'''
PREFERENCE_LIMIT = 3

'''
    ADDITION_PREFERENCE_LIMIT: Ek kurs tercih limiti
'''
ADDITION_PREFERENCE_LIMIT = 1

'''
    ACCOMODATION_PREFERENCE_LIMIT: Konaklama tercih limiti
'''
ACCOMODATION_PREFERENCE_LIMIT = 1

'''
    USER_TYPES: Sistemden olusturulacak kullanicilarin turleri
'''
USER_TYPES = {"inst": "instructor", "stu": "student", "hepsi": "hepsi"}

'''
    TRAINESS_PARTICIPATION_STATE: Kursiyerin kursa katilip katilmadigi
'''
TRAINESS_PARTICIPATION_STATE = [('-1', 'Kurs Yapılmadı'), ('0', 'Katılmadı'), ('1', 'Yarısına Katıldı'), ('2','Katıldı')]

'''
   GENDER: Profilde kullaniliyor
'''
GENDER = {'E': 'Erkek', 'K': 'Kadin', 'H': 'Hepsi'}

'''
   TRANSPORTATION: Egitmenin ulasim sekli
'''
TRANSPORTATION = {'0': 'Uçak', '1': 'Otobüs', '2': 'Araba', '3': 'Diğer'}

CKEDITOR_UPLOAD_PATH = "/static/"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'

'''
   TC Kimlik numarasını dogrularken kullanilan web servis
'''
TCKIMLIK_SORGULAMA_WS = "https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL"
'''
   REQUIRE_TRAINESS_APPROVE: Akademik Bilisimde katilimci kursa kabul edildikten sonra yeniden katılıp katılmayacağına
                            dair teyit alıyoruz. (True)
                            Kamp'ta öyle bir durum yok.(False)
'''
REQUIRE_TRAINESS_APPROVE = False
'''
    VIRTUAL_ENV_PATH: Uygulamanın Python virtualenv'nin kurulu oldugu dizinin yolu
'''
VIRTUAL_ENV_PATH = "venv/venv"
'''
    PROJECT_HOME_DIR: Uygulamanın ana dizini
'''
PROJECT_HOME_DIR = "/opt/ab-kurs-kayit/abkayit"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

from readconf import *

# SECURITY WARNING: keep the secret key used in production secret!
DJANGOSETTINGS = DjangoSettings()
SECRET_KEY = DJANGOSETTINGS.getsecretkey()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition
REQUIRE_UNIQUE_EMAIL = False

INSTALLED_APPS = (
    'longerusernameandemail',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.views',
    'abkayit',
    'userprofile',
    'training',
    'ckeditor',
    'ckeditor_uploader',
    'django_countries',
    'mailing',
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

DBCONF = DBconfig()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DBCONF.getdatabase(),
        'USER': DBCONF.getdbuser(),
        'PASSWORD': DBCONF.getdbpass(),
        'HOST': DBCONF.getdbhost(),
        'PORT'	: DBCONF.getdbport()
    }
}
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale/'), '/usr/local/lib/python2.7/dist-packages/django_countries/locale/')

LANGUAGE_CODE = 'tr'

# TIME_ZONE = 'GMT'
TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_L10N = True

USE_TZ = False
DATE_FORMAT = 'dMY'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
#STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
   os.path.join(BASE_DIR, 'static/'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates/')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

LOGIN_URL = "/"
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] [%(clientip)s - %(user)-8s] %(levelname)s [%(name)s:%(lineno)s]  %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': "[%(asctime)s] [%(user)-8s] %(levelname)s [%(name)s:%(lineno)s]  %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + "/logfile",
            'maxBytes': 2097152,
            'backupCount': 200,
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
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
UNIVERSITIES = [('Abant İzzet Baysal Üniversitesi (Bolu)', 'Abant İzzet Baysal Üniversitesi (Bolu)'),
                ('Abdullah Gül Üniversitesi (Kayseri)', 'Abdullah Gül Üniversitesi (Kayseri)'),
                (
                    'Acıbadem Üniversitesi (İstanbul)', 'Acıbadem Üniversitesi (İstanbul)'),
                (
                    'Adana Bilim ve Teknoloji Üniversitesi (Adana)', 'Adana Bilim ve Teknoloji Üniversitesi (Adana)'),
                ('Adıyaman Üniversitesi (Adıyaman)', 'Adıyaman Üniversitesi (Adıyaman)'),
                (
                    'Adnan Menderes Üniversitesi (Aydın)', 'Adnan Menderes Üniversitesi (Aydın)'),
                (
                    'Afyon Kocatepe Üniversitesi(Afyon)', 'Afyon Kocatepe Üniversitesi(Afyon)'),
                (
                    'Ağrı İbrahim Çeçen Üniversitesi(Ağrı)', 'Ağrı İbrahim Çeçen Üniversitesi(Ağrı)'),
                ('Ahi Evran Üniversitesi(Kırşehir)', 'Ahi Evran Üniversitesi(Kırşehir)'),
                ('Akdeniz Üniversitesi (Antalya)', 'Akdeniz Üniversitesi (Antalya)'),
                ('Aksaray Üniversitesi (Aksaray)', 'Aksaray Üniversitesi (Aksaray)'),
                ('Alanya Alaaddin Keykubat Üniversitesi (Antalya)', 'Alanya Alaaddin Keykubat Üniversitesi (Antalya)'),
                ('Amasya Üniversitesi (Amasya)', 'Amasya Üniversitesi (Amasya)'),
                ('Anadolu Üniversitesi (Eskişehir)', 'Anadolu Üniversitesi (Eskişehir)'),
                ('Ankara Sosyal Bilimler Üniversitesi(Ankara)', 'Ankara Sosyal Bilimler Üniversitesi(Ankara)'),
                ('Ankara Üniversitesi(Ankara)', 'Ankara Üniversitesi(Ankara)'),
                ('Ardahan Üniversitesi(Ardahan)', 'Ardahan Üniversitesi(Ardahan)'),
                ('Artvin Çoruh Üniversitesi(Artvin)', 'Artvin Çoruh Üniversitesi(Artvin)'),
                ('Ataşehir Adıgüzel Meslek Yüksekokulu(İstanbul)', 'Ataşehir Adıgüzel Meslek Yüksekokulu(İstanbul)'),
                ('Atatürk Üniversitesi (Erzurum)', 'Atatürk Üniversitesi (Erzurum)'),
                ('Atılım Üniversitesi (Ankara)', 'Atılım Üniversitesi (Ankara)'),
                ('Avrasya Üniversitesi (Trabzon)', 'Avrasya Üniversitesi (Trabzon)'),
                ('Avrupa Meslek Yüksek Okulu (İstanbul)', 'Avrupa Meslek Yüksek Okulu (İstanbul)'),
                ('Bahçeşehir Üniversitesi(İstanbul)', 'Bahçeşehir Üniversitesi(İstanbul)'),
                ('Balıkesir Üniversitesi(Balıkesir)', 'Balıkesir Üniversitesi(Balıkesir)'),
                ('Bandırma Onyedi Eylül Üniversitesi(Balıkesir)', 'Bandırma Onyedi Eylül Üniversitesi(Balıkesir)'),
                ('Bartın Üniversitesi(Bartın)', 'Bartın Üniversitesi(Bartın)'),
                ('Başkent Üniversitesi (Ankara)', 'Başkent Üniversitesi (Ankara)'),
                ('Batman Üniversitesi (Batman)', 'Batman Üniversitesi (Batman)'),
                ('Bayburt Üniversitesi (Bayburt)', 'Bayburt Üniversitesi (Bayburt)'),
                ('Beykent Üniversitesi (İstanbul)', 'Beykent Üniversitesi (İstanbul)'),
                ('Beykoz Lojistik Meslek Yüksek Okulu (İstanbul)', 'Beykoz Lojistik Meslek Yüksek Okulu (İstanbul)'),
                ('Bezm-i Âlem Vakıf Üniversitesi (İstanbul)', 'Bezm-i Âlem Vakıf Üniversitesi (İstanbul)'),
                ('Bilecik Şeyh Edebali Üniversitesi (Bilecik)', 'Bilecik Şeyh Edebali Üniversitesi (Bilecik)'),
                ('Bilkent Üniversitesi (Ankara)', 'Bilkent Üniversitesi (Ankara)'),
                ('Bingöl Üniversitesi (Bingöl)', 'Bingöl Üniversitesi (Bingöl)'),
                ('Biruni Üniversitesi (İstanbul)', 'Biruni Üniversitesi (İstanbul)'),
                ('Bitlis Eren Üniversitesi (Bitlis)', 'Bitlis Eren Üniversitesi (Bitlis)'),
                ('Boğaziçi Üniversitesi (İstanbul)', 'Boğaziçi Üniversitesi (İstanbul)'),
                ('Bozok Üniversitesi (Yozgat)', 'Bozok Üniversitesi (Yozgat)'),
                ('Bursa Orhangazi Üniversitesi (Bursa)', 'Bursa Orhangazi Üniversitesi (Bursa)'),
                ('Bursa Teknik Üniversitesi (Bursa)', 'Bursa Teknik Üniversitesi (Bursa)'),
                ('Bülent Ecevit Üniversitesi (Zonguldak)', 'Bülent Ecevit Üniversitesi (Zonguldak)'),
                ('Canik Başarı Üniversitesi (Samsun)', 'Canik Başarı Üniversitesi (Samsun)'),
                ('Celâl Bayar Üniversitesi (Manisa)', 'Celâl Bayar Üniversitesi (Manisa)'),
                ('Cumhuriyet Üniversitesi (Sivas)', 'Cumhuriyet Üniversitesi (Sivas)'),
                ('Çağ Üniversitesi (Tarsus-İçel)', 'Çağ Üniversitesi (Tarsus-İçel)'),
                ('Çanakkale Onsekiz Mart Üniversitesi(Çanakkale)', 'Çanakkale Onsekiz Mart Üniversitesi(Çanakkale)'),
                ('Çankaya Üniversitesi (Ankara)', 'Çankaya Üniversitesi (Ankara)'),
                ('Çankırı Karatekin Üniversitesi (Çankırı)', 'Çankırı Karatekin Üniversitesi (Çankırı)'),
                ('Çukurova Üniversitesi (Adana)', 'Çukurova Üniversitesi (Adana)'),
                ('Dicle Üniversitesi (Diyarbakır)', 'Dicle Üniversitesi (Diyarbakır)'),
                ('Doğuş Üniversitesi (İstanbul)', 'Doğuş Üniversitesi (İstanbul)'),
                ('Dokuz Eylül Üniversitesi (İzmir)', 'Dokuz Eylül Üniversitesi (İzmir)'),
                ('Dumlupınar Üniversitesi (Kütahya)', 'Dumlupınar Üniversitesi (Kütahya)'),
                ('Düzce Üniversitesi (Düzce)', 'Düzce Üniversitesi (Düzce)'),
                ('Ege Üniversitesi (İzmir)', 'Ege Üniversitesi (İzmir)'),
                ('Erciyes Üniversitesi (Kayseri)', 'Erciyes Üniversitesi (Kayseri)'),
                ('Erzincan Üniversitesi (Erzincan)', 'Erzincan Üniversitesi (Erzincan)'),
                ('Erzurum Teknik Üniversitesi (Erzurum)', 'Erzurum Üniversitesi (Erzurum)'),
                ('Eskişehir Osmangazi Üniversitesi (Eskişehir)', 'Eskişehir Osmangazi Üniversitesi (Eskişehir)'),
                ('Faruk Saraç Tasarım Meslek Yüksek Okulu (Bursa)', 'Faruk Saraç Tasarım Meslek Yüksek Okulu (Bursa)'),
                ('Fatih Sultan Mehmet Vakıf Üniversitesi (İstanbul)',
                 'Fatih Sultan Mehmet Vakıf Üniversitesi (İstanbul)'),
                ('Fatih Üniversitesi (İstanbul)', 'Fatih Üniversitesi (İstanbul)'),
                ('Fırat Üniversitesi (Elazığ)', 'Fırat Üniversitesi (Elazığ)'),
                ('Galatasaray Üniversitesi (İstanbul)', 'Galatasaray Üniversitesi (İstanbul)'),
                ('Gazi Üniversitesi (Ankara)', 'Gazi Üniversitesi (Ankara)'),
                ('Gaziantep Üniversitesi(Gaziantep)', 'Gaziantep Üniversitesi(Gaziantep)'),
                ('Gaziosmanpaşa Üniversitesi (Tokat)', 'Gaziosmanpaşa Üniversitesi (Tokat)'),
                ('Gebze Yüksek Teknoloji Enstitüsü(İzmit-Kocaeli)', 'Gebze Yüksek Teknoloji Enstitüsü(İzmit-Kocaeli)'),
                ('Gedik Üniversitesi (İstanbul)', 'Gedik Üniversitesi (İstanbul)'),
                ('Gediz Üniversitesi (İzmir)', 'Gediz Üniversitesi (İzmir)'),
                ('Giresun Üniversitesi (Giresun)', 'Giresun Üniversitesi (Giresun)'),
                ('Gümüşhane Üniversitesi (Gümüşhane)', 'Gümüşhane Üniversitesi (Gümüşhane)'),
                ('Hacettepe Üniversitesi (Ankara)', 'Hacettepe Üniversitesi (Ankara)'),
                ('Hakkari Üniversitesi (Hakkari)', 'Hakkari Üniversitesi (Hakkari)'),
                ('Haliç Üniversitesi(İstanbul)', 'Haliç Üniversitesi(İstanbul)'),
                ('Harran Üniversitesi (Şanlıurfa)', 'Harran Üniversitesi (Şanlıurfa)'),
                ('Hasan Kalyoncu Üniversitesi (Gaziantep)', 'Hasan Kalyoncu Üniversitesi (Gaziantep)'),
                ('Hitit Üniversitesi (Çorum)', 'Hitit Üniversitesi (Çorum)'),
                ('Iğdır Üniversitesi (Iğdır)', 'Iğdır Üniversitesi (Iğdır)'),
                ('Işık Üniversitesi (İstanbul)', 'Işık Üniversitesi (İstanbul)'),
                ('İnönü Üniversitesi (Malatya)', 'İnönü Üniversitesi (Malatya)'),
                ('İpek Üniversitesi (Ankara)', 'İpek Üniversitesi (Ankara)'),
                ('İskenderun Teknik Üniversitesi (Hatay)', 'İskenderun Teknik Üniversitesi (Hatay)'),
                ('İstanbul Arel Üniversitesi(İstanbul)', 'İstanbul Arel Üniversitesi(İstanbul)'),
                ('İstanbul Aydın Üniversitesi(İstanbul)', 'İstanbul Aydın Üniversitesi(İstanbul)'),
                ('İstanbul Üniversitesi(İstanbul)', 'İstanbul Üniversitesi(İstanbul)'),
                ('İstanbul Bilgi Üniversitesi(İstanbul)', 'İstanbul Bilgi Üniversitesi(İstanbul)'),
                ('İstanbul Bilim Üniversitesi(İstanbul)', 'İstanbul Bilim Üniversitesi(İstanbul)'),
                ('İstanbul Esenyurt Üniversitesi(İstanbul)', 'İstanbul Esenyurt Üniversitesi(İstanbul)'),
                ('İstanbul Gelişim Üniversitesi(İstanbul)', 'İstanbul Gelişim Üniversitesi(İstanbul)'),
                ('İstanbul Kavram Meslek Yüksek Okulu(İstanbul)', 'İstanbul Kavram Meslek Yüksek Okulu(İstanbul)'),
                ('İstanbul Kemerburgaz Üniversitesi(İstanbul)', 'İstanbul Kemerburgaz Üniversitesi(İstanbul)'),
                ('İstanbul Kültür Üniversitesi(İstanbul)', 'İstanbul Kültür Üniversitesi(İstanbul)'),
                ('İstanbul Medeniyet Üniversitesi(İstanbul)', 'İstanbul Medeniyet Üniversitesi(İstanbul)'),
                ('İstanbul Medipol Üniversitesi(İstanbul)', 'İstanbul Medipol Üniversitesi(İstanbul)'),
                ('İstanbul Rumeli Üniversitesi(İstanbul)', 'İstanbul Rumeli Üniversitesi(İstanbul)'),
                ('İstanbul Sabahattin Zaim Üniversitesi(İstanbul)', 'İstanbul Sabahattin Zaim Üniversitesi(İstanbul)'),
                ('İstanbul Şehir Üniversitesi(İstanbul)', 'İstanbul Şehir Üniversitesi(İstanbul)'),
                ('İstanbul Şişli Meslek Yüksek Okulu(İstanbul)', 'İstanbul Şişli Meslek Yüksek Okulu(İstanbul)'),
                ('İstanbul Teknik Üniversitesi(İstanbul)', 'İstanbul Teknik Üniversitesi(İstanbul)'),
                ('İstanbul Ticaret Üniversitesi(İstanbul)', 'İstanbul Ticaret Üniversitesi(İstanbul)'),
                ('İstanbul 29 Mayıs Üniversitesi(İstanbul)', 'İstanbul 29 Mayıs Üniversitesi(İstanbul)'),
                ('İzmir Yüksek Teknoloji Enstitüsü(İzmir)', 'İzmir Yüksek Teknoloji Enstitüsü(İzmir)'),
                ('İzmir Ekonomi Üniversitesi(İzmir)', 'İzmir Ekonomi Üniversitesi(İzmir)'),
                ('İzmir Katip Çelebi Üniversitesi(İzmir)', 'İzmir Katip Çelebi Üniversitesi(İzmir)'),
                ('İzmir Üniversitesi(İzmir)', 'İzmir Üniversitesi(İzmir)'),
                ('Kadir Has Üniversitesi(İstanbul)', 'Kadir Has Üniversitesi(İstanbul)'),
                ('Kafkas Üniversitesi (Kars)', 'Kafkas Üniversitesi (Kars)'),
                ('Kahramanmaraş Sütçü İmam Üniversitesi(Kahramanmaraş)',
                 'Kahramanmaraş Sütçü İmam Üniversitesi(Kahramanmaraş)'),
                ('Kanuni Üniversitesi (Adana)', 'Kanuni Üniversitesi (Adana)'),
                ('Kapadokya Meslek Yüksek Okulu (Nevşehir)', 'Kapadokya Meslek Yüksek Okulu Üniversitesi (Nevşehir)'),
                ('Karabuk Universitesi (Karabuk)', 'Karabuk Universitesi (Karabuk)'),
                ('Karadeniz Teknik Üniversitesi (Trabzon)', 'Karadeniz Teknik Üniversitesi (Trabzon)'),
                ('Karamanoğlu Mehmetbey Üniversitesi(Karaman)', 'Karamanoğlu Mehmetbey Üniversitesi(Karaman)'),
                ('Kastamonu Üniversitesi(Kastamonu)', 'Kastamonu Üniversitesi(Kastamonu)'),
                ('Kırıkkale Üniversitesi(Kırıkkale)', 'Kırıkkale Üniversitesi(Kırıkkale)'),
                ('Kırklareli Üniversitesi(Kırklareli)', 'Kırklareli Üniversitesi(Kırklareli)'),
                ('Kilis 7 Aralık Üniversitesi(Kilis)', 'Kilis 7 Aralık Üniversitesi(Kilis)'),
                ('Kocaeli Üniversitesi(Kocaeli-İzmit)', 'Kocaeli Üniversitesi(Kocaeli-İzmit)'),
                ('Koç Üniversitesi (İstanbul)', 'Koç Üniversitesi (İstanbul)'),
                ('Konya Gıda ve Tasarım Üniversitesi (Konya)', 'Konya Gıda ve Tasarım Üniversitesi (Konya)'),
                ('KTO Karatay Üniversitesi (Konya)', 'KTO Karatay Üniversitesi (Konya)'),
                ('Mardin Artuklu Üniversitesi (Mardin)', 'Mardin Artuklu Üniversitesi (Mardin)'),
                ('Maltepe Üniversitesi (İstanbul)', 'Maltepe Üniversitesi (İstanbul)'),
                ('Marmara Üniversitesi (İstanbul)', 'Marmara Üniversitesi (İstanbul)'),
                ('MEF Üniversitesi (İstanbul)', 'MEF Üniversitesi (İstanbul)'),
                ('Mehmet Akif Ersoy Üniversitesi (Burdur)', 'Mehmet Akif Ersoy Üniversitesi (Burdur)'),
                ('Melikşah Üniversitesi (Kayseri)', 'Melikşah Üniversitesi (Kayseri)'),
                ('Mersin Üniversitesi(Mersin-İçel)', 'Mersin Üniversitesi(Mersin-İçel)'),
                ('Mevlana Üniversitesi(Konya)', 'Mevlana Üniversitesi(Konya)'),
                ('Mimar Sinan Üniversitesi (İstanbul)', 'Mimar Sinan Üniversitesi (İstanbul)'),
                ('Muğla Üniversitesi(Muğla)', 'Muğla Üniversitesi(Muğla)'),
                ('Murat	Hüdavendigar Üniversitesi(İstanbul)', 'Murat Hüdavendigar Üniversitesi(İstanbul)'),
                ('Mustafa Kemal Üniversitesi (Hatay)', 'Mustafa Kemal Üniversitesi (Hatay)'),
                ('Muş Alparslan Üniversitesi(Muş)', 'Muş Alparslan Üniversitesi(Muş)'),
                ('Namık Kemal Üniversitesi(Tekirdağ)', 'Namık Kemal Üniversitesi(Tekirdağ)'),
                ('Necmettin Erbakan Üniversitesi(Konya)', 'Necmettin Erbakan Üniversitesi(Konya)'),
                ('Nevşehir Hacıbektaş Üniversitesi(Nevşehir)', 'Nevşehir Üniversitesi(Nevşehir)'),
                ('Niğde Üniversitesi(Niğde)', 'Niğde Üniversitesi(Niğde)'),
                ('Nişantaşı Üniversitesi(İstanbul)', 'Nişantaşı Üniversitesi(İstanbul)'),
                ('Nuh Naci Yazgan Üniversitesi(Kayseri)', 'Nuh Naci Yazgan Üniversitesi(Kayseri)'),
                ('Okan Üniversitesi(İstanbul)', 'Okan Üniversitesi(İstanbul)'),
                ('Ondokuz Mayıs Üniversitesi (Samsun)', 'Ondokuz Mayıs Üniversitesi (Samsun)'),
                ('Orta Doğu Teknik Üniversitesi (Ankara)', 'Orta Doğu Teknik Üniversitesi (Ankara)'),
                ('Ordu Üniversitesi (Ordu)', 'Ordu Üniversitesi (Ordu)'),
                ('Osmaniye Korkut Ata Üniversitesi (Osmaniye)', 'Osmaniye Korkut Ata Üniversitesi (Osmaniye)'),
                ('Özyeğin Üniversitesi (İstanbul)', 'Özyeğin Üniversitesi (İstanbul)'),
                ('Pamukkale Üniversitesi (Denizli)', 'Pamukkale Üniversitesi (Denizli)'),
                ('Piri Reis Üniversitesi (Denizli)', 'Piri Reis Üniversitesi (Denizli)'),
                ('Plato Meslek Yüksek Okulu (İstanbul)', 'Plato Meslek Yüksek Okulu (İstanbul)'),
                ('Recep Tayyip Erdoğan Üniversitesi (Rize)', 'Recep Tayyip Erdoğan Üniversitesi (Rize)'),
                ('Sabancı Üniversitesi(İstanbul)', 'Sabancı Üniversitesi(İstanbul)'),
                ('Sağlık Bilimleri Üniversitesi(İstanbul)', 'Sağlık Bilimleri Üniversitesi(İstanbul)'),
                ('Sakarya Üniversitesi(Sakarya-Adapazarı)', 'Sakarya Üniversitesi(Sakarya-Adapazarı)'),
                ('Sanko Üniversitesi (Gaziantep)', 'Sanko Üniversitesi (Gaziantep)'),
                ('Selahaddin Eyyubi Üniversitesi (Diyarbakır)', 'Selahaddin Eyyubi Üniversitesi (Diyarbakır)'),
                ('Selçuk Üniversitesi (Konya)', 'Selçuk Üniversitesi (Konya)'),
                ('Siirt Üniversitesi (Siirt)', 'Siirt Üniversitesi (Siirt)'),
                ('Sinop Üniversitesi (Sinop)', 'Sinop Üniversitesi (Sinop)'),
                ('Süleyman Demirel Üniversitesi (Isparta)', 'Süleyman Demirel Üniversitesi (Isparta)'),
                ('Süleyman Şah Üniversitesi (İstanbul)', 'Süleyman Şah Üniversitesi (İstanbul)'),
                ('Şırnak Üniversitesi (Şırnak)', 'Şırnak Üniversitesi (Şırnak)'),
                ('Şifa Üniversitesi (İzmir)', 'Şifa Üniversitesi (İzmir)'),
                ('Trakya Üniversitesi (Edirne)', 'Trakya Üniversitesi (Edirne)'),
                ('TED Üniversitesi (Ankara)', 'TED Üniversitesi (Ankara)'),
                ('TOBB Ekonomi ve Teknoloji Üniversitesi(Ankara)', 'TOBB Ekonomi ve Teknoloji Üniversitesi(Ankara)'),
                ('Toros Üniversitesi (Mersin)', 'Toros Üniversitesi (Mersin)'),
                ('Trakya Üniversitesi (Edirne)', 'Trakya Üniversitesi (Edirne)'),
                ('Tunceli Üniversitesi (Tunceli)', 'Tunceli Üniversitesi (Tunceli)'),
                ('Turgut Özal Üniversitesi (Ankara)', 'Turgut Özal Üniversitesi (Ankara)'),
                ('Türk Hava Kurumu Üniversitesi (Ankara)', 'Türk Hava Kurumu Üniversitesi (Ankara)'),
                ('Türk-Alman Üniversitesi (İstanbul)', 'Türk-Alman Üniversitesi (İstanbul)'),
                ('Ufuk Üniversitesi (Ankara)', 'Ufuk Üniversitesi (Ankara)'),
                ('Uludağ Üniversitesi (Bursa)', 'Uludağ Üniversitesi (Bursa)'),
                ('Uluslararası Antalya Üniversitesi (Antalya)', 'Uluslararası Antalya Üniversitesi (Antalya)'),
                ('Uşak Üniversitesi (Uşak)', 'Uşak Üniversitesi (Uşak)'),
                ('Üsküdar Üniversitesi (İstanbul)', 'Üsküdar Üniversitesi (İstanbul)'),
                ('Yalova Üniversitesi (Yalova)', 'Yalova Üniversitesi (Yalova)'),
                ('Yaşar Üniversitesi (İzmir)', 'Yaşar Üniversitesi (İzmir)'),
                ('Yeditepe Üniversitesi (İstanbul)', 'Yeditepe Üniversitesi (İstanbul)'),
                ('Yeni Yüzyıl Üniversitesi (İstanbul)', 'Yeni Yüzyıl Üniversitesi (İstanbul)'),
                ('Yıldız Teknik Üniversitesi (İstanbul)', 'Yıldız Teknik Üniversitesi (İstanbul)'),
                ('Yıldırım Beyazıt Üniversitesi (Ankara)', 'Yıldırım Beyazıt Üniversitesi (Ankara)'),
                ('Yüksek İhtisas Üniversitesi (Ankara)', 'Yüksek İhtisas Üniversitesi (Ankara)'),
                ('Yüzüncü Yıl Üniversitesi (Van)', 'Yüzüncü Yıl Üniversitesi (Van)'),
                ('Zirve Üniversitesi (Gaziantep)', 'Zirve Üniversitesi (Gaziantep)'),
                ('Zonguldak Karaelmas Üniversitesi(Zonguldak)', 'Zonguldak Karaelmas Üniversitesi(Zonguldak)'), ]
