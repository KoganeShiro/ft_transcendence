"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import os
from cryptography.fernet import Fernet

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get('HASHER_CODE')
OTP_ENC_KEY = os.environ.get('OTP_ENC_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'user_mgm.CustomUser'

# API Key

API_KEY = os.environ.get('API_KEY')

# Add social-auth-app-django settings
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/'
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
REDIRECT_URI = 'https://' + os.environ.get('HOSTNAME') + ':' + os.environ.get('PORT') + '/api/auth/complete/42/'

SOCIAL_AUTH_42_LOGIN_REDIRECT_URL = '/api/auth/get_token/'

SOCIAL_AUTH_42_KEY = os.environ.get('AUTH_CLIENT_ID')                     

SOCIAL_AUTH_42_SECRET = os.environ.get('AUTH_SECRET')
SOCIAL_AUTH_42_AUTHORIZATION_URL = 'https://api.intra.42.fr/oauth/authorize'
SOCIAL_AUTH_42_ACCESS_TOKEN_URL = 'https://api.intra.42.fr/oauth/token'
SOCIAL_AUTH_42_USER_DATA_URL = 'https://api.intra.42.fr/v2/me'
SOCIAL_AUTH_42_REDIRECT_URI = 'https://' + os.environ.get('HOSTNAME') + ':' + os.environ.get('PORT') + '/api/auth/complete/42/'
SOCIAL_AUTH_42_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_USER_MODEL = 'user_mgm.CustomUser'
SOCIAL_AUTH_42_SCOPE = ['public']
SOCIAL_AUTH_42_EXTRA_DATA = ['id', 'login', 'email', 'image']

# social login
AUTHENTICATION_BACKENDS = (
    #'social_core.backends.oauth.BaseOAuth2',
    'user_mgm.auth_backends.FortyTwoOAuth2', # 42 login
    'django.contrib.auth.backends.ModelBackend',  # Default Django auth
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'user_mgm.permissions.CookieJWTAuthentication',
        'user_mgm.permissions.APIKeyAuthentication',
    ), 

    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # ),

}

SOCIAL_AUTH_STATE_SESSION = False  # Prevent PSA from storing state in session
SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = []  # Ensure no fields are stored in session
SOCIAL_AUTH_PIPELINE_CACHE_KEY = "psa_pipeline_cache_{uid}"  # Store pipeline in cache
SOCIAL_AUTH_STORAGE = "social_django.models.DjangoStorage"  # Default DB storage, but can be overridden

SOCIAL_AUTH_PIPELINE = (  
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'user_mgm.social_pipeline.save_avatar',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'user_mgm.social_pipeline.generate_jwt_token',  
)
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user_mgm.apps.UserMgmConfig',
    'gamestats.apps.GamestatsConfig',
    'friends.apps.FriendsConfig',
    'django.db.backends.postgresql',    
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
 # added for social login
    'social_django', 
    'corsheaders',
   # for swagger
    'drf_yasg',
]


#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CORS_ALLOW_CREDENTIALS = True
# SECURE_SSL_REDIRECT = True

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=720),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',

    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

CSRF_COOKIE_HTTPONLY = False  # Ensure this is set to False
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'https://localhost:8000',
    'https://' + os.environ.get('HOSTNAME') + ':' + os.environ.get('PORT'),    
    'https://localhost',
    'https://localhost:1443',
    'http://back-end:8000',
]




MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
   # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'user_mgm.update_last_seen.UpdateLastSeenMiddleware',
    'corsheaders.middleware.CorsMiddleware',

]

CORS_ALLOWED_ORIGINS = [
    "https://" + os.environ.get('HOSTNAME') + ':' + os.environ.get('PORT'),
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get('POSTGRES_DB'),
        "USER": os.environ.get('POSTGRES_USER'),        
        "PASSWORD": os.environ.get('POSTGRES_PASSWORD'),
        "HOST": "postgres",        
        "PORT": "5432",
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
 #   {
 #       'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
 #   },
 #   {
 #       'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
 #   },
 #   {
 #       'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
 #   },
 #   {
 #       'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
 #   },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'CET'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# for testing purposes
# MEDIA_URL = '/media/'
MEDIA_ROOT = ('/mediafiles')

# for production
MEDIA_URL = "/media/"
# MEDIA_ROOT = BASE_DIR / "media"


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#SOCIAL_AUTH_PIPELINE = ('social_core.pipeline.debug.debug',)

SOCIAL_AUTH_USER_MODEL = 'user_mgm.CustomUser'
SOCIAL_AUTH_CREATE_USERS = True

import logging

logging.basicConfig(level=logging.DEBUG)
