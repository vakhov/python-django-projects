# -*- coding: utf-8 -*-

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Derter', 'derter@pixelion.ru'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'firmir',
        'USER': 'root',
        'PASSWORD': 'cthdthcnelbb',
        'HOST': 'localhost',
        'PORT': '',
    }
}

TIME_ZONE = 'Asia/Yekaterinburg'
LANGUAGE_CODE = 'ru-RU'

SITE_ID = 1

USE_I18N = False
USE_L10N = False

MEDIA_ROOT = '/work/media/firmir/sitefront/'
MEDIA_URL = '/media/'

STATIC_ROOT = '/work/dev/firmir/sitefront/static/'
STATIC_URL = '/static/'

# ADMIN_MEDIA_PREFIX = '/static/admin-media/'

STATICFILES_DIRS = ()

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = '6v5876rc^%*Ce56r7^V^&rv976rvC%sddb*5vdVBD*Ydsv7tdbntbvdcsTRDVUY%Dv8'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    '/work/dev/firmir/sitefront/templates/',
    '/work/dev/firmir/sitefront/widgets/templates/',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'pixelion.apps.widgets',
    'widgets'
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Widgets subclasses hierarchy
WIDGETS = {
#    "headers": {
#        "verbose_name": "Заголовки",
#        "package": "widgets.headers",
#        "items": [
#            ("H1", "Заголовок 1"),
#            ("H2", "Заголовок 2"),
#            ("H3", "Заголовок 3"),
#        ]
#    },
    "grid": {
        "verbose_name": "Сетка",
        "package": "widgets.grid",
        "items": [
            ("Grid_100", "100"),
            ("Grid_50_50", "50/50"),
            ("Grid_66_33", "66/33"),
            ("Grid_33_66", "33/66"),
            ("Grid_33_33_33", "33/33/33"),
        ]
    },
    "text": {
        "verbose_name": "Текст",
        "package": "widgets.text",
        "items": [
            ("SimpleText", "Абзац"),
            ("Cite", "Цитата"),
            ("Tip", "Заметка"),
            ("CharsTable", "Таблица характеристик"),
        ]
    },
    "lists": {
        "verbose_name": "Списки",
        "package": "widgets.lists",
        "items": [
            ("NumericList", "Нумерованный список"),
            ("UnorderedList", "Маркированный список"),
        ]
    }
}
