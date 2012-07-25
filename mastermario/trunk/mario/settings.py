import os
from settings_db import DATABASES

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Derter', 'derter@ekad.ru'),
    ('Succubi', 'succubi@pixelion.ru'),
)

MANAGERS = ADMINS

TIME_ZONE = 'Asia/Yekaterinburg'

LANGUAGE_CODE = 'ru-RU'

SITE_ID = 1

USE_I18N = True
USE_L10N = True

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.split(SITE_ROOT)[0]

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/work/media/mario/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/admin-media/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = '^rz_ma+s%*!at#f_q7_1m9(05-*8py3u_0x=aei(#da=pu^%d1'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.app_directories.load_template_source'
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'structure.middleware.StructureMiddleware',
    'aphaline.middleware.AphalineMiddleware',
    'seo.middleware.HashingMiddleware',
)

ROOT_URLCONF = 'mario.urls'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
    #'/usr/local/lib/python2.7/dist-packages/debug_toolbar/templates/',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    #'debug_toolbar',
    'genericm2m',
    'seo',
    'mptt',
    'structure',
    'articles',
    'widgets',
#     'catalogapp',
    'common',
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

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#     }
# }

LOGIN_REDIRECT_URL = '/'

FIELD_TYPES = ('BooleanField', 'CharField', 'IntegerField',
               'TextField', 'ChoiceField', 'MultipleChoiceField')

MONGODB_MANAGED_MODELS = ["catalogapp.Good"]

# DATABASE_ROUTERS = ["django_mongodb_engine.router.MongoDBRouter"]

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "utils.context_processors.seo_tags",
    "utils.context_processors.phone",
    "utils.context_processors.current_section",
    "utils.context_processors.structure",
    "aphaline.context_processors.aphaline_edit_mode",
)

INTERNAL_IPS = ('10.10.10.1',) 

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
)
