import os

# Make filepaths relative to settings.
ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)

DEBUG = True
TEMPLATE_DEBUG = True

JINJA_CONFIG = {}

SITE_ID = 1

SECRET_KEY = 'foobar'

TEST_RUNNER = 'django_nose.runner.NoseTestSuiteRunner'

DATABASES = {
    'default': {
        'NAME': 'test.db',
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django_nose',
    'south',
    'siteblocks'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'waffle.middleware.WaffleMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
)

WAFFLE_FLAG_DEFAULT = False
WAFFLE_SWITCH_DEFAULT = False
WAFFLE_SAMPLE_DEFAULT = False
WAFFLE_OVERRIDE = False
