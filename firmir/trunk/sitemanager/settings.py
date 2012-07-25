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

MEDIA_ROOT = '/work/media/firmir/sitemanager/'
MEDIA_URL = '/media/'

STATIC_ROOT = '/work/dev/firmir/sitemanager/static/'
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin-media/'

STATICFILES_DIRS = ()

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'p!lh118%otb6y&gob78V(&*567c*^&4c^&*$c7654*1hl&rz3uuh3#_23cq__qut2tuvq!s=d6_'

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
    '/work/dev/firmir/sitemanager/templates/'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
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