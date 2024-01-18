import os
from pathlib import Path

from datetime import timedelta  # JWT


DEBUG = True
# DEBUG = False
ALLOWED_HOSTS = []

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = os.path.join(BASE_DIR, 'static')


STATIC_URL = '/static/'
MEDIA_URL = '/media/'

if DEBUG:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    STATIC_ROOT = '/usr/share/nginx/html/static'
    MEDIA_ROOT = '/usr/share/nginx/html/media'


STATICFILES_DIRS = [
    (STATIC_DIR),
    ('account', STATIC_DIR + '/accounts/'),
    ('media', MEDIA_ROOT),
]


SECRET_KEY = 'django-insecure-=)mmqt#*+7f%libtv5zq(1p*e9hzqpmwphrg(8!lx%mso11aez'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'app',
    'accounts',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'django.contrib.humanize',

    'bootstrap_datepicker_plus',
    'django_cleanup',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'django.middleware.cache.UpdateCacheMiddleware',
    # 'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',

]

ROOT_URLCONF = 'mysite.urls'

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

                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# CACHES = {

#     'default':{

#         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',

#         'LOCATION': 'my_cache_table',

#     }
# }


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

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_I10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_EMAIL_VERIFICATION = 'none'


AUTH_USER_MODEL = 'accounts.CustomUser'  # 元
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False


NUMBER_GROUPING = 3  # カンマ区切り


# 自動ログアウト
# デフォルトは二週間後
# セッション時間
# SESSION_COOKIE_AGE = 60 * 60 #60 * 5 = 5分
# 最後にアクセスしてからの測定
SESSION_SAVE_EVERY_REQUEST = True