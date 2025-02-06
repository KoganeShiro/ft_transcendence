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

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f+&g!!lmxdld%5v!2&#q5oowy)p64m0pdys47ju9*g40r(z&kq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'user_mgm.CustomUser'

# social login

# Add social-auth-app-django settings
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/login-error/'
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
# REDIRECT_URI = 'https://localhost:1443/api/auth/complete/42/'
REDIRECT_URI = 'https://' + os.environ.get('HOSTNAME') + ':' + os.environ.get('PORT') + '/api/auth/complete/42/'

SOCIAL_AUTH_42_LOGIN_REDIRECT_URL = '/api/auth/get_token/'
SOCIAL_AUTH_42_KEY = 'u-s4t2ud-09ca6ba440f2f237ebfb37d37cfa280522f23fc10625ffe3eaf8639526912fd9'                      
SOCIAL_AUTH_42_SECRET = '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'
SOCIAL_AUTH_42_AUTHORIZATION_URL = 'https://api.intra.42.fr/oauth/authorize'
SOCIAL_AUTH_42_ACCESS_TOKEN_URL = 'https://api.intra.42.fr/oauth/token'
SOCIAL_AUTH_42_USER_DATA_URL = 'https://api.intra.42.fr/v2/me'
# SOCIAL_AUTH_42_REDIRECT_URI = 'https://localhost:1443/api/auth/complete/42/'
SOCIAL_AUTH_42_REDIRECT_URI = 'https://' + os.environ.get('HOSTNAME') + ':' + os.environ.get('PORT') + '/api/auth/complete/42/'
SOCIAL_AUTH_42_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_USER_MODEL = 'user_mgm.CustomUser'
#SOCIAL_AUTH_42_OAUTH2_WHITELISTED_DOMAINS = ['api.intra.42.fr', 'localhost:1443', 'localhost:8000', 'localhost']
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
    ), 
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    # ),    
}


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

   # 'user_mgm.social_pipeline.generate_jwt_token', 
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
   # 'dj_rest_auth',

    #'user_mgm',

]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=50),
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
    'https://localhost:443',
    'https://localhost:1443',
    'https://localhost',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'user_mgm.update_last_seen.UpdateLastSeenMiddleware',
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


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
# }

# remove the user details here...

#DATABASES = {
#    "default": {
#        "ENGINE": "django.db.backends.postgresql",
#        "NAME": "pongdb",
#        "USER": "postgres",
#        "PASSWORD": "password",
#        "HOST": "postgres",        
#        "PORT": "5432",
#    }
#}

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

MEDIA_URL = '/media/'
#MEDIA_ROOT = os.path.join(BASE_DIR, '/transcendence/media')
MEDIA_ROOT = ('./transcendence/media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#SOCIAL_AUTH_PIPELINE = ('social_core.pipeline.debug.debug',)

SOCIAL_AUTH_USER_MODEL = 'user_mgm.CustomUser'
SOCIAL_AUTH_CREATE_USERS = True

import logging

logging.basicConfig(level=logging.DEBUG)

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'root': {
#         'handlers': ['console'],
#         'level': 'DEBUG',
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'social_django': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         '': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }