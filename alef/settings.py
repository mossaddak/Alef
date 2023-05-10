
from pathlib import Path
import os
#from decouple import config
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = config('SECRET_KEY')
SECRET_KEY = 'django-insecure-xhqx%2z$qkcfb60h0u3*r7=t7rx)+7_g8o@xzz!dz%gdfj-t19'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG =config('DEBUG',default=True,cast=bool)
DEBUG = True

# ALLOWED_HOSTS = ['wsalef.herokuapp.com', '127.0.0.1','www.alefatelier.com']
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    #'whitenoise.runserver_nostatic',  # new
    'django.contrib.staticfiles',
    "crispy_forms",  # new
    "crispy_tailwind",  # new
    'accounts',  # new
    'category',  # new
    'store',  # new
    'carts',  # new
    'orders', #new
    'admin_honeypot', #new
    'storages', #new

]

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # new
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True

ROOT_URLCONF = 'alef.urls'
LOGIN_URL = '/login/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'category.context_processors.menu_links',  # new
                'category.context_processors.default_link',  # new
                'category.context_processors.default_hero',  # new
                'carts.context_processors.counter',  # new

            ],
        },
    },
]

WSGI_APPLICATION = 'alef.wsgi.application'

# custom user models
AUTH_USER_MODEL = 'accounts.Account'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {

#     'default': {

#         'ENGINE': 'django.db.backends.postgresql_psycopg2',

#         'NAME': 'localdb',

#         'USER': 'postgres',

#         'PASSWORD': '1q1q',

#         'HOST': 'localhost',

#         'PORT': '5432',

#     }

# }


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

TIME_ZONE = 'Europe/Athens'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (str(BASE_DIR.joinpath('static')),)
STATIC_ROOT = str(BASE_DIR.joinpath('staticfiles'))
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  # new

# # MEDIA_URL is the reference URL for browser to access the files over Http.
MEDIA_URL = '/media/'
# # MEDIA_ROOT is for server path to store files in the computer.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')  
# AWS_STORAGE_BUCKET_NAME = 'alefatelierbucket'
# AWS_S3_FILE_OVERWRITE = False 
# AWS_DEFAULT_ACL = None
# AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
# AWS_S3_OBJECT_PARAMETERS = {"CacheControl":"max-age=86400"}

# PUBLIC_MEDIA_LOCATION = 'media'
# #MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"
# DEFAULT_FILE_STORAGE = 'alef.storage_backends.MediaStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.ERROR: 'bg-red-600',
}

#smtp configuration
# EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST =config('EMAIL_HOST')
# EMAIL_PORT =config('EMAIL_PORT',cast=int)
# EMAIL_HOST_USER =config('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD=config('EMAIL_HOST_PASSWORD')
# EMAIL_USE_TLS=config('EMAIL_USE_TLS',cast=bool)

#smtp configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'#oke
EMAIL_HOST = 'smtp.gmail.com'#oke

EMAIL_PORT = '587'#oke
EMAIL_HOST_USER = ''#leave here your genuine email alefatelierbeta@gmail.com
EMAIL_HOST_PASSWORD = 'gzozkfosjaftnjqz'#leave here your genuine password of your email. keep it in mind, as the password should in encrypted condition 
EMAIL_USE_TLS = True#oke



db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Debugging in heroku live
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
#                        'pathname=%(pathname)s lineno=%(lineno)s ' +
#                        'funcname=%(funcName)s %(message)s'),
#             'datefmt': '%Y-%m-%d %H:%M:%S'
#         },
#         'simple': {
#             'format': '%(levelname)s %(message)s'
#         }
#     },
#     'handlers': {
#         'null': {
#             'level': 'DEBUG',
#             'class': 'logging.NullHandler',
#         },
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose'
#         }
#     },
#     'loggers': {
#         'testlogger': {
#             'handlers': ['console'],
#             'level': 'INFO',
#         }
#     }
# }

# DEBUG_PROPAGATE_EXCEPTIONS = True
# COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', False)