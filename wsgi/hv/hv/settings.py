# -*- coding: utf-8 -*-

"""
Django settings for hv project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

desarrollando = False if os.environ.get('OPENSHIFT_DATA_DIR', None) else True

DJ_PROJECT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
WSGI_DIR = os.path.dirname(BASE_DIR)
REPO_DIR = os.path.dirname(WSGI_DIR)
DATA_DIR = 'C:/Users/iLaptop/xampp/htdocs/Django/buy/data/' if desarrollando else os.environ.get('OPENSHIFT_DATA_DIR', BASE_DIR)

import sys
sys.path.append(os.path.join(REPO_DIR, 'libs'))
import secrets
SECRETS = secrets.getter(os.path.join(DATA_DIR, 'secrets.json'))
# ANIO_INICIO_CH = 2015  # CH: cuadro de honor
IDIOMAS_DISPONIBLES = ["es", "en"]
	# "es":
	# "en-US":
	# "pt-BR":
	# "ru-RU":
	# "hi":  # india?
	# "en-ZA":  # sudafrica  or "af" or "zu":
	# "zh-CN":
	# "fr-FR":
	# "da-DE":  # or "de-DE":

## django los esconde las variables que contienen: API, KEY, PASS, SECRET, SIGNATURE, TOKEN
desarrollando_en_paypal = True

if desarrollando_en_paypal:
	ACCESO_API_PAYPAL = {
		"HEADERS_API": {
			"X-PAYPAL-SECURITY-USERID": "v11-presidente_api1.hotmail.com",
			"X-PAYPAL-SECURITY-PASSWORD": "YDJ4JY78B4PJ49NM",
			"X-PAYPAL-SECURITY-SIGNATURE": "AFcWxV21C7fd0v3bYYYRCpSSRl31A19Xg5YCxz26FXh2mHNU6iUanMTY",
			"X-PAYPAL-APPLICATION-ID": "APP-80W284485P519543T",
			"X-PAYPAL-REQUEST-DATA-FORMAT": "JSON",
			"X-PAYPAL-RESPONSE-DATA-FORMAT": "JSON",
		},
		"CORREO_API": "v11-presidente@hotmail.com",
		"URL_REFUND": "https://svcs.sandbox.paypal.com/AdaptivePayments/Refund",
		"URL_EXECUTE": "https://svcs.sandbox.paypal.com/AdaptivePayments/ExecutePayment",
		"URL_PAY": "https://svcs.sandbox.paypal.com/AdaptivePayments/Pay",
		"URL_GOPAY": "https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_ap-payment&paykey="
	}
else:
	ACCESO_API_PAYPAL = {
		"HEADERS_API": {
			"X-PAYPAL-SECURITY-USERID": "luistena.developer_api1.hotmail.com",
			"X-PAYPAL-SECURITY-PASSWORD": "2KYBFK4XZRP6CAUB",
			"X-PAYPAL-SECURITY-SIGNATURE": "A3gtadA.qm-wBsRRzcYXSiDI4VENAX3WSHA1VSmNyC10FMVOPDPc28wb",
			"X-PAYPAL-APPLICATION-ID": "APP-80W284485P519543T",
			"X-PAYPAL-REQUEST-DATA-FORMAT": "JSON",
			"X-PAYPAL-RESPONSE-DATA-FORMAT": "JSON",
		},
		"CORREO_API": "luistena.developer@hotmail.com",
		"URL_REFUND": "https://svcs.paypal.com/AdaptivePayments/Refund",
		"URL_EXECUTE": "https://svcs.paypal.com/AdaptivePayments/ExecutePayment",
		"URL_PAY": "https://svcs.paypal.com/AdaptivePayments/Pay",
		"URL_GOPAY": "https://www.paypal.com/cgi-bin/webscr?cmd=_ap-payment&paykey="
	}

from decimal import Decimal
COMISION_PAYPAL = {"ganancia": Decimal("5.4"), "neto": Decimal("0.3")}
COMISION_HV = 30
#PRECIO_POR_DOLAR = 1000


SECRET_KEY = SECRETS['secret_key']
DEBUG = True  # False


# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

LOCALE_PATHS = (
	'postman/locale',
	'C:/Users/iLaptop/xampp/htdocs/Django/buy/wsgi/hv/postman/locale'
)

from socket import gethostname

ALLOWED_HOSTS = [
	gethostname(), # For internal OpenShift load balancer security purposes.
	os.environ.get('OPENSHIFT_APP_DNS',""), # Dynamically map to the OpenShift gear name.
	#'example.com', # First DNS alias (set up in the app)
	#'www.example.com', # Second DNS alias (set up in the app)
]

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'postman',
	'geoservicios',
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.locale.LocaleMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'hv.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'Plantillas/')],
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

WSGI_APPLICATION = 'hv.wsgi.application'

if desarrollando:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',  # 'django.db.backends.sqlite3',
			'NAME': 'buy',  # os.path.join(DATA_DIR, 'buy'),
			'USER': 'postgres',
			'PASSWORD': 'qwerty2',
			'HOST': 'localhost',
			'PORT': '5432'
		}
	}
else:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'NAME': 'buy',
			'USER': 'adminci3pyaj',
			'PASSWORD': 'ftijnkv9DCWE',
			'HOST': os.environ.get('OPENSHIFT_POSTGRESQL_DB_HOST', ""),
			'PORT': os.environ.get('OPENSHIFT_POSTGRESQL_DB_PORT', "") # '5432'
		}
	}

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
if desarrollando:
	STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
	STATICFILES_DIRS = (
		os.path.join(WSGI_DIR, 'static/'),
	)
else:
	STATIC_ROOT = os.path.join(WSGI_DIR, 'multimedia/')


if desarrollando:
	MEDIA_URL = '/media/'
	MEDIA_ROOT = os.path.join(DATA_DIR, 'subidos/')  # '~/hv/Multimedia/images/'
	# xPENSAR: deberia dejar esto es DATA_DIR ya q es donde se guardan lo del usr


ADMIN_MEDIA_PREFIX = '/multimedia/admin/'

# EMAIL_HOST = ""  # xHACER: que  SMTP server  me brinda OpenShift pa los correos?
# EMAIL_PORT = 25


#####################
# solo para jugar con ipython
# DJANGO_SETTINGS_MODULE = 'hv.settings'

# super usr=jefe , pw= jefe@a.a
POSTMAN_AUTO_MODERATE_AS = True
