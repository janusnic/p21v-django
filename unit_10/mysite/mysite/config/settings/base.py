"""
Base settings and globals.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

from os.path import abspath, basename, dirname, join, normpath
from os import listdir
from sys import path


########## PATH CONFIGURATION
# Absolute filesystem path to the config directory:
CONFIG_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the project directory:
PROJECT_ROOT = dirname(CONFIG_ROOT)

# Absolute filesystem path to the django repo directory:
DJANGO_ROOT = dirname(PROJECT_ROOT)

# Project name:
PROJECT_NAME = basename(PROJECT_ROOT).capitalize()

# Project folder:
PROJECT_FOLDER = basename(PROJECT_ROOT)

# Project domain:
PROJECT_DOMAIN = '%s.com' % PROJECT_NAME.lower()

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(CONFIG_ROOT)
########## END PATH CONFIGURATION


########## EMAIL CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = '[%s] ' % PROJECT_NAME

# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = 'Serverbot <dev@%s>' % PROJECT_DOMAIN
########## END EMAIL CONFIGURATION


########## MANAGER CONFIGURATION
# See https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Dev Team', 'Dev Team <dev@%s>' % PROJECT_DOMAIN),
)

# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
########## END MANAGER CONFIGURATION


########## APP CONFIGURATION
DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
    'authtools',
    'django_extensions',
    'django_rq',
    'floppyforms',
    'pipeline',
)

PROJECT_APPS = (
    'apps.accounts',
)

EXTENSION_APPS = (
    'extensions.authtools',
    'extensions.django_rq',
    'extensions.rq_scheduler',
)

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS + EXTENSION_APPS
########## END APP CONFIGURATION


########## MIDDLEWARE CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
########## END MIDDLEWARE CONFIGURATION


########## MIGRATIONS CONFIGURATION
MIGRATION_MODULES = {
    'sites': 'extensions.sites.migrations'
}
########## END MIGRATIONS CONFIGURATION


########## DEBUG CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = STAGING = False
########## END DEBUG CONFIGURATION


########## SECRET CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key should only be used for development and testing.
SECRET_KEY = r"lle*l7qn&!tog)$1n$=#op1rst%e!7k8t-k@wm&&v@msnuo6ud"
########## END SECRET CONFIGURATION


########## FIXTURE CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    normpath(join(PROJECT_ROOT, 'fixtures')),
)
########## END FIXTURE CONFIGURATION


########## GENERAL CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'Europe/Kiev'

# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'ua'

# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
########## END GENERAL CONFIGURATION


########## TEMPLATE CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/templates/
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            normpath(join(PROJECT_ROOT, 'templates')),
            normpath(join(PROJECT_ROOT, 'extensions')),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'string_if_invalid': 'NULL',
        },
    },
]
########## END TEMPLATE CONFIGURATION


########## MEDIA CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(PROJECT_ROOT, 'media'))

# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION


########## STATIC FILE CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(PROJECT_ROOT, 'public'))

# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    normpath(join(PROJECT_ROOT, 'static')),
)

STATICFILES_FINDERS_IGNORE = [
    '*.scss',
    '*.coffee',
    '*.map',
    '*.html',
    '*.txt',
    '*tests*',
    '*uncompressed*',
]

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
    'pipeline.finders.CachedFileFinder',
)

# STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'
########## END STATIC FILE CONFIGURATION


########## PIPELINE CONFIGURATION
# https://django-pipeline.readthedocs.org/en/latest/configuration.html
def pipeline_source_filenames(filetype):
    source_filenames = []
    staticfiles_path = normpath(join(PROJECT_ROOT, 'static'))
    for folder in ('lib', 'build'):
        path = '%s/%s/%s' % (staticfiles_path, filetype, folder)
        source_filenames += ['%s/%s/%s' % (filetype, folder, filename) for filename in listdir(path) if filename.endswith('.%s' % filetype)]
    return tuple(source_filenames)

PIPELINE_CSS = {
    'master': {
        'source_filenames': pipeline_source_filenames('css'),
        'output_filename': 'css/master.css',
        'variant': 'datauri',
    },
}

PIPELINE_JS = {
    'master': {
        'source_filenames': pipeline_source_filenames('js'),
        'output_filename': 'js/master.js',
        'extra_context': {
            'async': True,
        },
    }
}
########## END PIPELINE CONFIGURATION


########## URL CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'config.urls'
########## END URL CONFIGURATION


########## LOGIN/LOGOUT CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = '/'

# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = '/login/'

# https://docs.djangoproject.com/en/dev/ref/settings/#logout-url
LOGOUT_URL = '/logout/'
########## END LOGIN/LOGOUT CONFIGURATION


########## WSGI CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'
########## END WSGI CONFIGURATION


########## USER MODEL CONFIGURATION
AUTH_USER_MODEL = 'accounts.User'
########## END USER MODEL CONFIGURATION


########## TESTING CONFIGURATION
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
########## END TESTING CONFIGURATION


########## LOGGING CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'production_only': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'development_only': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'readable_sql': {
            '()': 'project_runpy.ReadableSqlFilter',
        },
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)-8s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%m/%d/%Y %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)-8s [%(name)s:%(lineno)s] %(message)s',
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'default': {
            'level': 'DEBUG',
            'class': 'config.lib.colorstreamhandler.ColorStreamHandler',
        },
        'console_dev': {
            'level': 'DEBUG',
            'filters': ['development_only'],
            'class': 'config.lib.colorstreamhandler.ColorStreamHandler',
            'formatter': 'simple',
        },
        'console_prod': {
            'level': 'INFO',
            'filters': ['production_only'],
            'class': 'config.lib.colorstreamhandler.ColorStreamHandler',
            'formatter': 'simple',
        },
        'file_log': {
            'level': 'DEBUG',
            'filters': ['development_only'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': join(DJANGO_ROOT, 'logs/log.log'),
            'maxBytes': 1024 * 1024,
            'backupCount': 3,
            'formatter': 'verbose',
        },
        'file_sql': {
            'level': 'DEBUG',
            'filters': ['development_only'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': join(DJANGO_ROOT, 'logs/sql.log'),
            'maxBytes': 1024 * 1024,
            'backupCount': 3,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['production_only'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
    },
    # Catch-all modules that use logging
    # Writes to console and file on development, only to console on production
    'root': {
        'handlers': ['console_dev', 'console_prod', 'file_log'],
        'level': 'DEBUG',
    },
    'loggers': {
        # Write all SQL queries to a file
        'django.db.backends': {
            'handlers': ['file_sql'],
            'filters': ['readable_sql'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # Email admins when 500 error occurs
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}
########## END LOGGING CONFIGURATION
