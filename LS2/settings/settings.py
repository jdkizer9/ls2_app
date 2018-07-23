"""
Django settings for LS2 project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from django.core.exceptions import ImproperlyConfigured
from . import database_settings
from . import authentication_settings
from . import admin_portal_settings
from . import study_management_portal_settings
from . import participant_api_settings
from . import health_check_settings
from study_management import database_routers

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
# LS2_DEBUG env variable is a string,
# ignore case, check that it matches true for debug
DEBUG = os.environ.get('LS2_DEBUG', 'false').lower() == 'true'

# SECURITY WARNING: keep the secret key used in production secret!
LS2_HOST = os.environ.get('LS2_HOSTNAME')
SECRET_KEY = os.environ.get('DJANGO_SECRET')
if SECRET_KEY == None or len(SECRET_KEY) < 32:
    raise ImproperlyConfigured(
        "Invalid secret key."
    )

# we use use a proxy so we need to set use forwarded HOST,
# see https://docs.djangoproject.com/en/2.0/topics/security/#host-header-validation
# see https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-USE_X_FORWARDED_HOST
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
if DEBUG == False:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

#SECURITY SETTINGS

SECURE_HSTS_SECONDS = 300
# SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

if DEBUG==False:
    if LS2_HOST != None:
        ALLOWED_HOSTS = [LS2_HOST]
        CSRF_TRUSTED_ORIGINS = [LS2_HOST]
    else:
        raise ImproperlyConfigured("No Host Specified. Check the LS2_HOSTNAME environment variable")
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']
    if os.environ.get('LS2_EXTRA_DEBUG_HOSTS') != None:
        extra_hosts = os.environ.get('LS2_EXTRA_DEBUG_HOSTS').split(',')
        ALLOWED_HOSTS = ALLOWED_HOSTS + extra_hosts
        CSRF_TRUSTED_ORIGINS = extra_hosts

if DEBUG:

    from fnmatch import fnmatch
    class glob_list(list):
        def __contains__(self, key):
            for elt in self:
                if fnmatch(key, elt): return True
            return False

    INTERNAL_IPS = glob_list(['*'])

REST_FRAMEWORK_ENABLED = False

ADMIN_PORTAL_ENABLE = os.environ.get('LS2_ADMIN_PORTAL_ENABLE', 'false').lower() == 'true'
if ADMIN_PORTAL_ENABLE:
    extra_admin_portal_settings = admin_portal_settings.get_additional_settings(os.environ)
    for (key, value) in extra_admin_portal_settings.items():
        globals()[key] = value

STUDY_MANAGEMENT_PORTAL_ENABLE = os.environ.get('LS2_STUDY_MANAGEMENT_PORTAL_ENABLE', 'false').lower() == 'true'
if STUDY_MANAGEMENT_PORTAL_ENABLE:
    extra_study_management_portal_settings = study_management_portal_settings.get_additional_settings(os.environ)
    for (key, value) in extra_study_management_portal_settings.items():
        globals()[key] = value

PARTICIPANT_API_ENABLE = os.environ.get('LS2_PARTICIPANT_API_ENABLE', 'false').lower() == 'true'
if PARTICIPANT_API_ENABLE:
    REST_FRAMEWORK_ENABLED = True
    extra_participant_api_settings = participant_api_settings.get_additional_settings(os.environ)
    for (key, value) in extra_participant_api_settings.items():
        globals()[key] = value

# Set Up Admins for error notification
ADMIN_NAME = os.environ.get('LS2_ADMIN_NAME')
ADMIN_EMAIL = os.environ.get('LS2_ADMIN_EMAIL')
if ADMIN_NAME != None and ADMIN_EMAIL != None:
    ADMINS = [(ADMIN_NAME, ADMIN_EMAIL)]
else:
    ADMINS = []

INSTALLED_APPS = [
    'study_management.apps.StudyManagementConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'easyaudit',
    'session_security',
    'health_check',
    'health_check.db',
]

if REST_FRAMEWORK_ENABLED:
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.TokenAuthentication',
        ),
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        )
    }

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'easyaudit.middleware.easyaudit.EasyAuditMiddleware',
    'session_security.middleware.SessionSecurityMiddleware',
]

PASSWORD_HASHERS = [
    'study_management.password_hashers.StrongBCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

auth_settings = authentication_settings.get_auth_settings(os.environ)
for (key, value) in auth_settings.items():
    globals()[key] = value

ROOT_URLCONF = 'LS2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'LS2.wsgi.application'

SITE_ID = 1

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST = os.environ.get('LS2_EMAIL_HOST')
# EMAIL_PORT = 587

##Need to conver this to int
if os.environ.get('LS2_EMAIL_PORT') != None:
    EMAIL_PORT = int(os.environ.get('LS2_EMAIL_PORT'))
    
# EMAIL_HOST_USER = '*******************'
EMAIL_HOST_USER = os.environ.get('LS2_EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = '*******************'
EMAIL_HOST_PASSWORD = os.environ.get('LS2_EMAIL_HOST_PASSWORD')

if os.environ.get('LS2_EMAIL_USE_TLS') != None:
    EMAIL_USE_TLS = os.environ.get('LS2_EMAIL_USE_TLS').lower() == 'true'

if os.environ.get('LS2_EMAIL_USE_SSL') != None:
    EMAIL_USE_SSL = os.environ.get('LS2_EMAIL_USE_SSL').lower() == 'true'
# DEFAULT_FROM_EMAIL = '*******************'
DEFAULT_FROM_EMAIL = os.environ.get('LS2_FROM_EMAIL')
SERVER_EMAIL = os.environ.get('LS2_FROM_EMAIL')

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# the backup status endpoint will return 500 if a backup hasnt been completed
# less than 48 hours ago
LS2_BACKUP_AGE_MINS_MAX = int(os.environ.get('LS2_BACKUP_AGE_MINS_MAX', 48*60))
LS2_BACKUP_HEALTH_CHECK_ENABLED = os.environ.get('LS2_BACKUP_HEALTH_CHECK_ENABLED', 'true').lower() == 'true'

HEALTH_CHECK_ENABLED = os.environ.get('LS2_HEALTH_CHECK_ENABLED', 'false').lower() == 'true'
if HEALTH_CHECK_ENABLED:
    health_settings = health_check_settings.get_settings(os.environ)
    for (key, value) in health_settings.items():
        globals()[key] = value

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'default': {
            'level':'DEBUG',
            'filters': ['require_debug_true'],
            'class':'study_management.logging.TimedCompressedRotatingFileHandler',
            'when': 'W6',
            'filename': '/logs/default.log',
            'backupCount': 13,
            'formatter':'standard',
        },
        'django': {
            'level':'DEBUG',
            'class':'study_management.logging.TimedCompressedRotatingFileHandler',
            'when': 'W6',
            'filename': '/logs/django.log',
            'backupCount': 13,
            'formatter':'standard',
        },
        'request': {
            'level':'DEBUG',
            'class':'study_management.logging.TimedCompressedRotatingFileHandler',
            'when': 'W6',
            'filename': '/logs/request.log',
            'backupCount': 13,
            'formatter':'standard',
        },
        'server': {
            'level':'DEBUG',
            'class':'study_management.logging.TimedCompressedRotatingFileHandler',
            'when': 'W6',
            'filename': '/logs/server.log',
            'backupCount': 13,
            'formatter':'standard',
        },
        'audit': {
            'level':'DEBUG',
            'class':'study_management.logging.TimedCompressedRotatingFileHandler',
            'when': 'W6',
            'filename': '/logs/audit.log',
            'backupCount': 13,
            'formatter':'standard',
        },
        'mail_admins': {
            'level': 'WARNING',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django': {
            'handlers': ['django'],
            'level': 'INFO',
            'propagate': True
        },
        'django.request': {
            'handlers': ['request', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.server': {
            'handlers': ['server'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}


extra_database_settings = database_settings.get_database_settings(os.environ)
for (key, value) in extra_database_settings.items():
    globals()[key] = value

# DATABASES = database_settings.get_databases(os.environ)
# if DATABASES == None:
#     raise ImproperlyConfigured("Databases improperly configured")
#
# DATABASE_ROUTERS = database_settings.get_database_routers(os.environ)

# easyaudit settings
# NOTE: We patched easy audit a bit due to errors in the request signal
# see here: https://github.com/soynatan/django-easy-audit/pull/36
# DJANGO_EASY_AUDIT_WATCH_MODEL_EVENTS = False
# DJANGO_EASY_AUDIT_WATCH_AUTH_EVENTS = False
# DJANGO_EASY_AUDIT_WATCH_REQUEST_EVENTS = False
DJANGO_EASY_AUDIT_ADMIN_SHOW_MODEL_EVENTS = False
DJANGO_EASY_AUDIT_ADMIN_SHOW_AUTH_EVENTS = False
DJANGO_EASY_AUDIT_ADMIN_SHOW_REQUEST_EVENTS = False
DJANGO_EASY_AUDIT_UNREGISTERED_CLASSES_EXTRA = [
    'study_management.PasswordChangeEvent',
    'study_management.Datapoint',
    'authtoken.Token',
    'db.TestModel',
]

DJANGO_EASY_AUDIT_UNREGISTERED_URLS_EXTRA = [
    r'^/ht/'
]


DJANGO_EASY_AUDIT_REMOTE_ADDR_HEADER = 'HTTP_X_REAL_IP'

# LS2_SECURITY_PASSWORD_AGE_LIMIT_MINUTES = 10
# LS2_SECURITY_PASSWORD_AGE_WARN_MINUTES = 5
LS2_SECURITY_ADDITIONAL_BCRYPT_ROUNDS = int(os.environ.get('LS2_SECURITY_ADDITIONAL_BCRYPT_ROUNDS', 2))

PARTICIPANT_ACCOUNT_GENERATION_ENABLED = os.environ.get('PARTICIPANT_ACCOUNT_GENERATION_ENABLED', 'false').lower() == 'true'
PARTICIPANT_ACCOUNT_GENERATOR_LOGIN_RATE_LIMIT_ENABLED = os.environ.get('PARTICIPANT_ACCOUNT_GENERATOR_LOGIN_RATE_LIMIT_ENABLED', 'true').lower() == 'true'
PARTICIPANT_ACCOUNT_GENERATOR_RATE_LIMIT_REQUESTS = int(os.environ.get('PARTICIPANT_ACCOUNT_GENERATOR_RATE_LIMIT_REQUESTS', 5))
PARTICIPANT_ACCOUNT_GENERATOR_RATE_LIMIT_WINDOW_MINUTES = int(os.environ.get('PARTICIPANT_ACCOUNT_GENERATOR_RATE_LIMIT_WINDOW_MINUTES', 1))
PARTICIPANT_ACCOUNT_GENERATOR_RATE_LIMIT_TIMEOUT_MINUTES = int(os.environ.get('PARTICIPANT_ACCOUNT_GENERATOR_RATE_LIMIT_TIMEOUT_MINUTES', 1))

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# SESSION_SECURITY_EXPIRE_AFTER = 10
# SESSION_SECURITY_WARN_AFTER = 5

# password configuration setting
PASSWORD_RESET_TIMEOUT_DAYS = 0

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'study_management.password_validation.ReusedPasswordValidator',
        'OPTIONS': {
            'min_generations': 3,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

PARTICIPANT_ACCOUNT_GENERATOR_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/static'
STATICFILES_DIRS = [ os.path.join(BASE_DIR, "static") ]
