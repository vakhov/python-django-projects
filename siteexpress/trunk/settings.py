import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Derter', 'derter@ekad.ru'),
    ('Succubi', 'succubi@pixelion.ru'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'flora_se',
        'USER': 'root',
        'PASSWORD': 'cthdthcnelbb',
        'HOST': 'localhost',
        'PORT': '',
    }
}

TIME_ZONE = 'Asia/Yekaterinburg'
LANGUAGE_CODE = 'ru-RU'
SITE_ID = 1

EMAIL_HOST = 'mail.ekad.ru'
EMAIL_HOST_USER = 'siteexpress@pixelion.ru'
EMAIL_HOST_PASSWORD = 'tratata'
#EMAIL_PORT = 587
#EMAIL_USE_TLS = True

USE_I18N = True
USE_L10N = True

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

MEDIA_ROOT = '/work/dev/flora/media/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin-media/'
SESSION_SAVE_EVERY_REQUEST= True

STATICFILES_DIRS = (
    '/work/dev/flora/app/static/new/',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "aphaline.context_processors.aphaline_edit_mode",
    "utils.context_processors.phone",
    "utils.context_processors.phone_flora",
    "utils.context_processors.footer_zone",
    "utils.context_processors.current_section",
    "utils.context_processors.structure",
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'x%+2+bxbj$sy%i5iegtm(1spss--wys0e$_&pr(%ib+4=zz+))'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'structure.middleware.StructureMiddleware',
    'aphaline.middleware.AphalineMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'filebrowser',
    'tinymce',
    'django.contrib.admin',
    'aphaline',
    'management',
    #'siteexpress',
    'structure',
    'widgets',
    'se'
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

TINYMCE_JS_URL = STATIC_URL + "tiny_mce/tiny_mce.js"
TINYMCE_JS_ROOT = STATIC_URL + "tiny_mce"
TINYMCE_SPELLCHECKER=False
TINYMCE_PLUGINS = [
    
]

TINYMCE_DEFAULT_CONFIG={
    'theme' : "simple", #simple, advanced
    'plugins' : ",".join(TINYMCE_PLUGINS), # django-cms
    'language' : 'ru',
    "theme_advanced_buttons1" : "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,styleselect,formatselect,fontselect,fontsizeselect,|,spellchecker",
    "theme_advanced_buttons2" : "cut,copy,paste,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,image,cleanup,code,|,forecolor,backcolor,|,insertfile,insertimage",
    "theme_advanced_buttons3" : "tablecontrols,|,hr,removeformat,visualaid,|,sub,sup,|,charmap,emotions,iespell,media,advhr",
    'theme_advanced_toolbar_location' : "top",
    'theme_advanced_toolbar_align' : "left",
    'theme_advanced_statusbar_location' : "bottom",
    'theme_advanced_resizing' : True,
    'table_default_cellpadding': 2,
    'table_default_cellspacing': 2,
    'cleanup_on_startup' : False,
    'cleanup' : False,
    'paste_auto_cleanup_on_paste' : False,
    'paste_block_drop' : False,
    'paste_remove_spans' : False,
    'paste_strip_class_attributes' : False,
    'paste_retain_style_properties' : "",
    'forced_root_block' : False,
    'force_br_newlines' : False,
    'force_p_newlines' : False,
    'remove_linebreaks' : False,
    'convert_newlines_to_brs' : False,
    'inline_styles' : False,
    'relative_urls' : False,
    'formats' : {
        'alignleft' : {'selector' : 'p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li,table,img', 'classes' : 'align-left'},
        'aligncenter' : {'selector' : 'p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li,table,img', 'classes' : 'align-center'},
        'alignright' : {'selector' : 'p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li,table,img', 'classes' : 'align-right'},
        'alignfull' : {'selector' : 'p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li,table,img', 'classes' : 'align-justify'},
        'strikethrough' : {'inline' : 'del'},
        'italic' : {'inline' : 'em'},
        'bold' : {'inline' : 'strong'},
        'underline' : {'inline' : 'u'}
    },
    'pagebreak_separator' : "",
    # Drop lists for link/image/media/template dialogs
    'template_external_list_url': 'lists/template_list.js',
    'external_link_list_url': 'lists/link_list.js',
    'external_image_list_url': 'lists/image_list.js',
    'media_external_list_url': 'lists/media_list.js',
    #
    #'file_browser_callback':'tinyDjangoBrowser'
}
