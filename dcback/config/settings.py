import os, sys, subprocess, json, pickle
from datetime import timedelta
from pathlib import Path
# from eshop.Utilss.utils import DictObj
sys.path.insert(0, '/home/dcback')
from eshop.hc_vault.vault_client import vault_Client


class DictObj:
    def __init__(self, in_dict:dict):
        assert isinstance(in_dict, dict)
        for key, val in in_dict.items():
            if isinstance(val, (list, tuple)):
               setattr(self, key, [DictObj(x) if isinstance(x, dict) else x for x in val])
            else:
               setattr(self, key, DictObj(val) if isinstance(val, dict) else val)
               
    def to_dict(self):
        out_dict = {}
        for key, val in self.__dict__.items():
            if isinstance(val, DictObj):
                out_dict[key] = val.to_dict()
            elif isinstance(val, (list, tuple)):
                out_dict[key] = [item.to_dict() if isinstance(item, DictObj) else item for item in val]
            else:
                out_dict[key] = val
        return out_dict


ENV_DICT = DictObj(vault_Client.get_secret('dcdev'))
BASE_DIR = Path(__file__).resolve().parent.parent

# setENV()
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENV_DICT.SECRET_KEY
# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = int(vault_Client.get_secret('dcdev', 'DEBUG'))
DEBUG = True


# ALLOWED_HOSTS = vault_Client.get_secret('dcdev', 'ALLOWED_HOSTS').split(',')
# SESSION_COOKIE_HTTPONLY = True





ALLOWED_HOSTS = [
    "digicod.eu",
    ".digicod.eu",
    "localhost",
    "127.0.0.1",
]



# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# SESSION_COOKIE_AGE = 3000000
SESSION_COOKIE_NAME = "sessionid"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "Lax"

CSRF_COOKIE_NAME = "csrftoken"
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "Lax"

INSTALLED_APPS = [
    'django_hosts',
    "channels",
    'daphne',
    'dbbackup',
    'eshop',
    'api',
    'apps.accounts',
    'apps.shop',
    'apps.orders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    # 'rest_framework_simplejwt.token_blacklist',
    # 'rest_framework_simplejwt',
    'djoser',
    'cryptcurr',
    'api.dyn_api',
]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/0",  # Redis-Datenbank 0
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
    "websocket": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/1",  # Redis-Datenbank 1
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "SERIALIZER_CLASS": "django_redis.serializers.pickle.PickleSerializer",
        },
    },
}

'Redis-Konfiguration'
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
    "alternate": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379, 1)],  # Datenbank 1
        },
    },
}

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    "config.middleware.local_only.LocalOnlyPathsMiddleware",
    "config.middleware.local_only.LocalOnlyDomainMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # ###############
    'config.middleware.middlewares.SetAuthorizationHeaderMiddleware',
    # ###############
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # ################
    'django_hosts.middleware.HostsResponseMiddleware',
]

############################################
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = (
# 'http://localhost:5174',
# )
CORS_ALLOWED_ORIGINS = [
    '.digicod.eu',
    '*'
]
CORS_REPLACE_HTTPS_REFERER = True
CSRF_TRUSTED_ORIGINS = [
    "https://.digicod.eu",
    "https://api.digicod.eu",
    "https://rest.digicod.eu",
]

CORS_ALLOW_HEADERS = [ 
    "accept", 
    "referer", 
    "accept-encoding",
    "Accept-Language",
    "authorization",
    "connection",
    "content-Length",
    "content-type", 
    "cookie",
    "Next-Action",
    "Next-Router-State-Tree",
    "host",
    "dnt", 
    "origin",
    "referer",
    "user-agent", 
    "x-csrftoken", 
    "x-sessionid", 
    "Sec-Fetch-Dest",
    "Sec-Fetch-Site",
    "x-requested-with",
    "sec-fetch-mode",
    "sec-ch-ua",
    "sec-ch-ua-mobile",
    "sec-ch-ua-platform",
    'x-forwarded-for',
    'x-forwarded-proto',
    'x-envoy-internal',
    'x-request-id',
    'x-envoy-expected-rq-timeout-ms',
    'x-forwarded-host',
    'x-forwarded-port',
    "response-xxxxcodes",
]

CORS_EXPOSE_HEADERS = ['Set-Cookie']
CORS_ALLOWED_HOSTS = [
    'https://front.digicod.eu',
    '*'
]


CORS_ALLOW_CREDENTIALS = True  # Erlaubt das Senden von Cookies


CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
##################################################
# COOKIE_SAMESITE = 'None'
# COOKIE_SECURE = True  # Erforderlich für SameSite=None
# Session Cookies
# SESSION_COOKIE_SAMESITE = 'None'
# SESSION_COOKIE_SECURE = True  # Erforderlich für SameSite=None


# CSRF Cookies
# CSRF_COOKIE_SAMESITE = 'None'
# CSRF_COOKIE_SECURE = True  # Erforderlich für SameSite=None

DEFAULT_HOST = 'shop'
PARENT_HOST = ".digicod.eu"
ROOT_HOSTCONF = 'config.hosts'
ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates',]
        ,
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

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = "config.asgi.application"

DATABASES = {
'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': ENV_DICT.DB_NAME,
        'USER': ENV_DICT.DB_USER,
        'PASSWORD': ENV_DICT.DB_PASSWORD,
        'HOST': ENV_DICT.DB_HOST,
        'PORT': ENV_DICT.DB_PORT,
    }
}
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': '/media/user/store/django/'}


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# exakten Host aus dem netcup Webhosting-/Mail-Interface übernehmen
EMAIL_HOST = 'mx2e33.netcup.net'
# üblich für Submission mit STARTTLS
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

EMAIL_HOST_USER = 'support@digicod.eu'
EMAIL_HOST_PASSWORD = ENV_DICT.EMAIL_HOST_PASSWORD

DEFAULT_FROM_EMAIL = "Digicod <support@digicod.eu>"
SERVER_EMAIL = "admin@digicod.eu"
EMAIL_TIMEOUT = 20


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

WEBAUTHN_RP_ID = "front.digicod.eu"
WEBAUTHN_RP_NAME = "DIGICOD Webshop"
WEBAUTHN_ORIGIN = "https://front.digicod.eu"

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'django_admin_staticfiles/'

STATICFILES_DIRS = tuple(
    path for path in (
        BASE_DIR / 'cdnx/eshop-ui/build/static/',
        BASE_DIR / 'cdnx/admin-ui/build/static/',
    )
    if path.exists()
)

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'cdnx/media/'

# Syntax: URI -> Import_PATH

DYNAMIC_API = {
    # SLUG -> Import_PATH 
    'product'  : "apps.shop.models.Product",
    'brand'  : "apps.shop.models.Brand",

    'category'  : "apps.shop.models.Category",
    'payment'  : "apps.shop.models.Payment",
    'cart'  : "apps.shop.models.Cart",
}

DYNAMIC_API2 = {
    # SLUG -> Import_PATH 
    'product'  : "eshop.models.Product",
    'orders'  : "eshop.models.Orders",
}

# DYNAMIC_API = {
#     "product": {
#         "model": "eshop.models.Product",
#         "serializer": "api.serializers.SZ.ProductS",
#         "pagination": True,
#     },
#     "brand": {
#         "model": "eshop.models.Brand",
#         "serializer": "api.serializers.SZ.ProductS",
#         "pagination": True,
#     },
#     "category": {
#         "model": "eshop.models.Category",
#         "serializer": "api.serializers.SZ.CategoryS",
#         "pagination": False,
#     },
# }


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
PASSWORD_RESET_TIMEOUT = 60 * 30
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        # 'rest_framework.renderers.BrowsableAPIRenderer',
        # 'drf_renderer_xlsx.renderers.XLSXRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES':[
        'rest_framework.authentication.TokenAuthentication'
        ],
    
    'AUTHENTICATION_BACKENDS': {
        'django.contrib.auth.backends.AllowAllUsersModelBackend',
        "django.contrib.auth.backends.ModelBackend",
        # "sesame.backends.ModelBackend",
    },
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    #     # 'rest_framework.permissions.CurrentUserOrAdmin',
    #     'rest_framework.permissions.IsAuthenticated',
    #     'rest_framework.permissions.AllowAny',
    #     'rest_framework.permissions.IsAdminUser',
    # ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'DEFAULT_PAGINATION_CLASS': 'eshop_api.pagination.CustomPagination',
    # # 'PAGE_SIZE': 15,
        
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'sesame.backends.ModelBackend',
]

DJOSER = {
    'DOMAIN': 'front.digicod.eu',
    'SITE_NAME': 'DIGICOD',
    'LOGIN_FIELD':'email',
    'PASSWORD_RESET_CONFIRM_URL': 'password_reset/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'username/reset/confirm/{uid}/{token}',
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'ACTIVATION_URL': 'user_activation/{uid}/{token}',
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'SEND_ACTIVATION_EMAIL': True,
    'TOKEN_MODEL': 'eshop.models.CustomToken',
    # 'TOKEN_MODEL': 'rest_framework.authtoken.models.Token',
    'SERIALIZERS': {
        # 'current_user': 'eshop.serializers.CustomerSerializer',
        'user_create': 'eshop.serializers.RegisterSerializer',
        'user': 'eshop.serializers.UserSerializer',
        'current_user': 'eshop.serializers.UserSerializer',
        'token_create': 'eshop.serializers.CustomTokenCreateSerializer',
        
        
    },
    'CONSTANTS': {
        # 'messages': 'djoser.constants.Messages',
        'messages': 'eshop.djoser_messages.CustomMessages'
    },
    'EMAIL': {
        'activation': 'djoser.email.ActivationEmail',
        'confirmation': 'djoser.email.ConfirmationEmail',
        'password_reset': 'djoser.email.PasswordResetEmail',
        'password_changed_confirmation': 'djoser.email.PasswordChangedConfirmationEmail',
        'username_changed_confirmation': 'djoser.email.UsernameChangedConfirmationEmail',
        'username_reset': 'djoser.email.UsernameResetEmail',
    },
    
    'PERMISSIONS': {
        'activation': ['rest_framework.permissions.AllowAny'],
        'password_reset': ['rest_framework.permissions.AllowAny'],
        'password_reset_confirm': ['rest_framework.permissions.AllowAny'],
        'set_password': ['rest_framework.permissions.IsAdminUser'],
        'username_reset': ['rest_framework.permissions.AllowAny'],
        'username_reset_confirm': ['rest_framework.permissions.AllowAny'],
        'set_username': ['rest_framework.permissions.IsAdminUser'],
        'user_create': ['rest_framework.permissions.AllowAny'],
        'user_delete': ['rest_framework.permissions.IsAdminUser'],
        'user': ['rest_framework.permissions.IsAuthenticated'],
        'user_list': ['rest_framework.permissions.IsAdminUser'],
        'token_create': ['rest_framework.permissions.AllowAny'],
        'token_destroy': ['rest_framework.permissions.IsAuthenticated'],
    }
}



TEMPORAL_ADDRESS = getattr(ENV_DICT, "TEMPORAL_ADDRESS", None) or "temporal.loc:7233"
TEMPORAL_NAMESPACE = getattr(ENV_DICT, "TEMPORAL_NAMESPACE", None) or "default"
TEMPORAL_TASK_QUEUE_PREPAIDFORGE_SYNC = getattr(
    ENV_DICT,
    "TEMPORAL_TASK_QUEUE_PREPAIDFORGE_SYNC",
    None,
) or "prepaidforge-product-sync"
TEMPORAL_PREPAIDFORGE_SYNC_SCHEDULE_ID = getattr(
    ENV_DICT,
    "TEMPORAL_PREPAIDFORGE_SYNC_SCHEDULE_ID",
    None,
) or "prepaidforge-products-every-5-minutes"

import os, logging
from loguru import logger
class PropagateHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        logging.getLogger(record.name).handle(record)

logger.add(PropagateHandler(), format="{message}")
logger.add(sys.stderr, format="{time} {level} {message}", level="DEBUG")
logger.add("debug.log", rotation="10 MB", retention="10 days", level="DEBUG", format="{time} {level} {message}", backtrace=True, diagnose=True)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "daphne_debug.log"),
            "formatter": "verbose",
        },
        "console": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "channels": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
        "daphne": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
