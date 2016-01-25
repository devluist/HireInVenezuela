# -*- coding: utf-8 -*-

"""
Django settings for hv project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
DJ_PROJECT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
WSGI_DIR = os.path.dirname(BASE_DIR)
REPO_DIR = os.path.dirname(WSGI_DIR)
DATA_DIR = 'C:/Users/iLaptop/xampp/htdocs/Django/buy/data' if (type(os.environ.get('DEBUG')) == type(None) or os.environ.get('DEBUG') == False ) else os.environ.get('OPENSHIFT_DATA_DIR', BASE_DIR)

import sys
sys.path.append(os.path.join(REPO_DIR, 'libs'))
import secrets
SECRETS = secrets.getter(os.path.join(DATA_DIR, 'secrets.json'))

from decimal import Decimal
MI_CORREO_PAYPAL = "v11-presidente@hotmail.com"  # "luistena.developer@hotmail.com"
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
#PRECIO_POR_DOLAR = 1000
COMISION_PAYPAL = {"ganancia": Decimal("5.4"), "neto": Decimal("0.3")}
COMISION_HV = 30
# ANIO_INICIO_CH = 2015  # CH: cuadro de honor
HEADERS_PAYPAL = {
	"X-PAYPAL-SECURITY-USERID": "v11-presidente_api1.hotmail.com",
	"X-PAYPAL-SECURITY-PASSWORD": "YDJ4JY78B4PJ49NM",
	"X-PAYPAL-SECURITY-SIGNATURE": "AFcWxV21C7fd0v3bYYYRCpSSRl31A19Xg5YCxz26FXh2mHNU6iUanMTY",
	"X-PAYPAL-APPLICATION-ID": "APP-80W284485P519543T",
	"X-PAYPAL-REQUEST-DATA-FORMAT": "JSON",
	"X-PAYPAL-RESPONSE-DATA-FORMAT": "JSON",
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRETS['secret_key']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True   #xPENSAR: esto estaba en la mia lo dejo?


#######################################################################################3
#######################################################################################3 
#######################################################################################3


from socket import gethostname

ALLOWED_HOSTS = [
	gethostname(), # For internal OpenShift load balancer security purposes.
	os.environ.get('OPENSHIFT_APP_DNS'), # Dynamically map to the OpenShift gear name.
	#'example.com', # First DNS alias (set up in the app)
	#'www.example.com', # Second DNS alias (set up in the app)
]

# Application definition

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

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(DATA_DIR, 'db.sqlite3'),
	}
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(WSGI_DIR, 'multimedia/')
# STATICFILES_DIRS = (
	# os.path.join(BASE_DIR, 'postman/static/'),
# )

##################################
##################################

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(DATA_DIR, 'subidos/')  # '~/hv/Multimedia/images/'
# xPENSAR: deberia dejar esto es DATA_DIR ya q es donde se guardan lo del usr


# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/multimedia/admin/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_HOST = ""  # xHACER: que host me brinda OpenShift pa los correos?
# EMAIL_PORT = 25


#####################
# xDEPURAR: solo para jugar con ipython
# DJANGO_SETTINGS_MODULE = 'hv.settings'

# super usr=jefe , pw= jefe@a.a
POSTMAN_AUTO_MODERATE_AS = True
