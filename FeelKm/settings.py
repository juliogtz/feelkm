# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import dj_database_url

#BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONTENT_TYPES = ['application/pdf', 'image/jpeg', 'image/png']  # .pdf, .jpeg and .png

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+ms(lk3*#5#s_lfsi(q*vz@*#mkfc1n&m)losu@yn%yy_vl4r!'


ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'south',
    'api',
    'websearch',
    'usrs'

)

STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'


ADMIN_MEDIA_PREFIX = '/statics/'

MEDIA_ROOT = 'media'
MEDIA_URL = 'media/'

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)


REST_FRAMEWORK = {

    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'PAGINATE_BY':10

}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
)

ROOT_URLCONF = 'FeelKm.urls'


#WSGI_APPLICATION = 'FeelKm.wsgi'

#WSGI_APPLICATION = 'FeelKm.wsgi'



DATABASES = {'default': dj_database_url.config(default='postgres://lviqbnyffylarx:mSwShplq7isnfSHjhARNoIz45q@ec2-54-243-48-227.compute-1.amazonaws.com:5432/d5rn6km9c8lnvn')}
#DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

#STATIC_URL = 'http://127.0.0.1:8000/static/'
#STATIC_ROOT = '/Users/Julio/PycharmProjects/FeelKm/static/'

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'statics'
STATIC_URL = 'statics/'

#STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, 'static'),
#)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

DEBUG = True
TEMPLATE_DEBUG = True

