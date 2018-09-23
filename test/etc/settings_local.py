# -*- coding: utf-8 -*-
import sys

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'forget_me_not_dev',
        'USER': 'forget_me_not_dev',
        'PASSWORD': 'shiul9Qu',
        'HOST': '',
        'PORT': '',
    }
}
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test_database'
    }

DEFAULT_FROM_EMAIL = '776166@gmail.com'

INTERNAL_IPS = [
    '195.91.244.98',
]

if DEBUG == True:
    ALLOWED_HOSTS = [
        'forget-me-not.dev.madget.net',
    ]
else:
    ALLOWED_HOSTS = [
        'forget-me-not.pro.madget.net'
    ]

SECRET_KEY = '3heo@s^7t&#036ph0)t=bsa4_8*4x=+p+#6_ib%eo50ps41-8@'
