# -*- coding: utf-8 -*-

"""
Django settings for hv project.
"""
## django los esconde las variables que contienen: API, KEY, PASS, SECRET, SIGNATURE, TOKEN
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

import os

desarrollando = False if os.environ.get('OPENSHIFT_DATA_DIR', None) else True
desarrollando_en_paypal = True # TODO: AFTER PAYPAL REFACTOR, CHANGE THIS TO FALSE



DJ_PROJECT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
WSGI_DIR = os.path.dirname(BASE_DIR)
REPO_DIR = os.path.dirname(WSGI_DIR)
DATA_DIR = os.path.join(REPO_DIR, 'data/') if desarrollando else os.environ.get('OPENSHIFT_DATA_DIR', BASE_DIR)

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
from decimal import Decimal
COMISION_PAYPAL = {"ganancia": Decimal("5.4"), "neto": Decimal("0.3")}
COMISION_HV = 30
#PRECIO_POR_DOLAR = 1000
SECRET_KEY = SECRETS['secret_key']

LOCALE_PATHS = (
	'postman/locale',
	os.path.join(BASE_DIR, 'postman/locale')
)

#from socket import gethostname

ALLOWED_HOSTS = [
	"*",
	#gethostname(), # For internal OpenShift load balancer security purposes.
	#os.environ.get('OPENSHIFT_APP_DNS',""), # Dynamically map to the OpenShift gear name.
	#"dolarTrabajado.Tk",
	#"www.dolarTrabajado.Tk",
	#"hireInVenezuela.com",
	#"www.hireInVenezuela.com",
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

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

#####################
# solo para jugar con ipython
DJANGO_SETTINGS_MODULE = 'hv.settings'

POSTMAN_AUTO_MODERATE_AS = True


if desarrollando:
	DEBUG = True
	STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
	STATICFILES_DIRS = (
		os.path.join(WSGI_DIR, 'static/'),
	)
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.sqlite3',
			'NAME': os.path.join(DATA_DIR, 'hireinve.db'),

			#'ENGINE': 'django.db.backends.postgresql_psycopg2',
			#'NAME': 'hireinve',
			#'USER': 'postgres',
			#'PASSWORD': 'qwerty2',
			#'HOST': 'localhost',
			#'PORT': '5432'
		}
	}
	MULTIMEDIA_EN = {"css":"/static/css/", "jsjq":"/static/js/", "jsboot":"/static/js/"}
	URL_SITIO = "http://localhost:8000/"
	MEDIA_URL = '/media/'
	MEDIA_ROOT = 'media/'
	EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
	MUESTRA_ERRORES_SMTP = True

else:
	DEBUG = False
	STATIC_ROOT = os.path.join(WSGI_DIR, 'multimedia/')
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.sqlite3',
			'NAME': os.path.join(DATA_DIR, 'hireinve.db'),

			# 'ENGINE': 'django.db.backends.postgresql_psycopg2',
			# 'NAME': 'hireinve',
			# 'USER': '',
			# 'PASSWORD': '',
			# 'HOST': os.environ.get('OPENSHIFT_POSTGRESQL_DB_HOST', ""),
			# 'PORT': os.environ.get('OPENSHIFT_POSTGRESQL_DB_PORT', "")
		}
	}
	MULTIMEDIA_EN = {"css":"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/", "jsjq":"https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/", "jsboot":"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/"}
	URL_SITIO = "http://hireInVenezuela.com/"
	MUESTRA_ERRORES_SMTP = False
	EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
	EMAIL_USE_TLS = True
	EMAIL_HOST = 'smtp-mail.outlook.com'
	EMAIL_HOST_USER = 'correo@mail.com'
	EMAIL_HOST_PASSWORD = 'tuclavesegura'
	EMAIL_PORT = 587


if desarrollando_en_paypal:
	ACCESO_API_PAYPAL = {
		"HEADERS_API": {
			"X-PAYPAL-SECURITY-USERID": "correo_fake_api1.dominio.com",
			"X-PAYPAL-SECURITY-PASSWORD": "123456",
			"X-PAYPAL-SECURITY-SIGNATURE": "1234567890",
			"X-PAYPAL-APPLICATION-ID": "APP-123456789",
			"X-PAYPAL-REQUEST-DATA-FORMAT": "JSON",
			"X-PAYPAL-RESPONSE-DATA-FORMAT": "JSON",
		},
		"CORREO_API": "developer@fake.com",
		"CORREO_USR_API": "",
		# "URL_REFUND": "https://svcs.paypal.com/AdaptivePayments/Refund",
		# "URL_EXECUTE": "https://svcs.paypal.com/AdaptivePayments/ExecutePayment",
		# "URL_PAY": "https://svcs.paypal.com/AdaptivePayments/Pay",
		# "URL_GOPAY": "https://www.paypal.com/cgi-bin/webscr?cmd=_ap-payment&paykey="

		"URL_REFUND": "http://localhost:3000/refund",
		"URL_EXECUTE": "http://localhost:3000/executePayment",
		"URL_PAY": "http://localhost:3000/pay",
		"URL_GOPAY": "https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_ap-payment&paykey="
	}
else:
	ACCESO_API_PAYPAL = {
		"HEADERS_API": {
			"X-PAYPAL-SECURITY-USERID": "correo_fake_api1.dominio.com",
			"X-PAYPAL-SECURITY-PASSWORD": "123456",
			"X-PAYPAL-SECURITY-SIGNATURE": "1234567890",
			"X-PAYPAL-APPLICATION-ID": "APP-123456789",
			"X-PAYPAL-REQUEST-DATA-FORMAT": "JSON",
			"X-PAYPAL-RESPONSE-DATA-FORMAT": "JSON",
		},
		"CORREO_API": "developer@fake.com",
		"CORREO_USR_API": "",
		"URL_REFUND": "https://svcs.paypal.com/AdaptivePayments/Refund",
		"URL_EXECUTE": "https://svcs.paypal.com/AdaptivePayments/ExecutePayment",
		"URL_PAY": "https://svcs.paypal.com/AdaptivePayments/Pay",
		"URL_GOPAY": "https://www.paypal.com/cgi-bin/webscr?cmd=_ap-payment&paykey="
	}
