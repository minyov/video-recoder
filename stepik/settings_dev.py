DEBUG = True

SECRET_KEY = '$s!czwb9f$lgmwr*0qt#kc9&8r!ldebjz=5m9=0up-ud*_#5oe'

ALLOWED_HOSTS = ['*']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'stepik',
        'USER': 'stepik',
        'PASSWORD': 'stepik',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

CELERY_BROKER_URL = 'amqp://stepik:stepik@localhost:5672/stepik'
CELERY_RESULT_BACKEND = 'amqp://stepik:stepik@localhost:5672/stepik'
