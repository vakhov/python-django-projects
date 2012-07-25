import os
from settings_local import DATABASES, MEDIA_ROOT

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Derter', 'derter@ekad.ru'),
    ('Succubi', 'succubi@pixelion.ru'),
    ('Rain', 'rain@pixelion.ru'),
)

MANAGERS = ADMINS



EMAIL_HOST = 'alex.vakhov@gmail.com'
#EMAIL_PORT = 587
EMAIL_HOST_USER = 'wachow@yandex.ru'
EMAIL_HOST_PASSWORD = 'ptvfafpfy'
#EMAIL_USE_TLS = True

#MAIL SEND
#FROM
MAIL_FROM = 'alex.vakhov@gmail.com'
#TO
MAIL_TO = 'alex.vakhov@gmail.com'

TIME_ZONE = 'Asia/Yekaterinburg'

LANGUAGE_CODE = 'ru-RU'

SITE_ID = 1

DELTA_DATE = 30

USE_I18N = True
USE_L10N = True

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

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
ADMIN_MEDIA_PREFIX = '/static/admin/'

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
)

SECRET_KEY = '^rz_ma+s%*!at#f_q7_1m9(05-*8py3u_0x=aei(#da=pu^%d1'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'structure.middleware.StructureMiddleware',
    'aphaline.middleware.AphalineMiddleware',
    'seo.middleware.HashingMiddleware',
)

ROOT_URLCONF = 'urls'

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
    'seo',
    'structure',
    'widgets',
    'common',
    'questanswer',
    'catalog',
    'articles',
    'text',
    'title',
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

LOGIN_REDIRECT_URL = '/'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "utils.context_processors.seo_tags",
    "utils.context_processors.phone",
    "utils.context_processors.banner",
    "utils.context_processors.footer",
    "utils.context_processors.crumbs",
    "utils.context_processors.current_section",
    "utils.context_processors.current_path",
    "utils.context_processors.structure",
    "utils.context_processors.main_links",
    "utils.context_processors.basket_summary_info",
    "aphaline.context_processors.aphaline_edit_mode",
    "text.context_processors.textonpage",
    "catalog.context_processors.filter",
    "catalog.context_processors.nova",
)
