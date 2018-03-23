from django.conf import settings
from django.contrib.auth import password_validation

LOGIN_RATE_LIMIT_ENABLED = getattr(settings, 'LS2_SECURITY_LOGIN_RATE_LIMIT_ENABLED', True)
LOGIN_RATE_LIMIT_FAILED_ATTEMPTS = getattr(settings, 'LS2_SECURITY_LOGIN_RATE_LIMIT_FAILED_ATTEMPTS', 5)
LOGIN_RATE_LIMIT_WINDOW_MINUTES = getattr(settings, 'LS2_SECURITY_LOGIN_RATE_LIMIT_WINDOW_MINUTES', 5)
LOGIN_RATE_LIMIT_TIMEOUT_MINUTES = getattr(settings, 'LS2_SECURITY_LOGIN_RATE_LIMIT_TIMEOUT_MINUTES', 30)

ADDITIONAL_BCRYPT_ROUNDS = getattr(settings, 'LS2_SECURITY_ADDITIONAL_BCRYPT_ROUNDS', 4)

PASSWORD_AGE_LIMIT_MINUTES = getattr(settings, 'LS2_SECURITY_PASSWORD_AGE_LIMIT_MINUTES', 90*24*60)
PASSWORD_AGE_WARN_MINUTES = getattr(settings, 'LS2_SECURITY_PASSWORD_AGE_WARN_MINUTES', 80*24*60)

BACKUP_HEALTH_CHECK_ENABLED = getattr(settings, 'LS2_BACKUP_HEALTH_CHECK_ENABLED', True)
BACKUP_AGE_MINS_MAX = getattr(settings, 'LS2_BACKUP_AGE_MINS_MAX', 2*24*60)

DEFAULT_PARTICIPANT_ACCOUNT_GENERATOR_PASSWORD_VALIDATORS = [
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

PARTICIPANT_ACCOUNT_GENERATOR_PASSWORD_VALIDATORS = password_validators = password_validation.get_password_validators(getattr(settings, 'PARTICIPANT_ACCOUNT_GENERATOR_PASSWORD_VALIDATORS', DEFAULT_PARTICIPANT_ACCOUNT_GENERATOR_PASSWORD_VALIDATORS))
