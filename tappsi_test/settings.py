"""
Django settings for tappsi_test project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(u=26%h&gl67gd+(gsjkf8a+6d4(s(89lfj$qj7%+utlh%kg)r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'oauth2_provider',
    'rest_framework',
    'django_user_agents',
    'rest_framework_swagger',
    'tappsi_api',
    'lettuce.django'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
)

ROOT_URLCONF = 'tappsi_test.urls'

WSGI_APPLICATION = 'tappsi_test.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'database/tappsi.db'),
    }
}

# if 'test' in sys.argv:
    # DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer'
    ),
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    'PAGINATE_BY': 10,                 # Default to 10
    'PAGINATE_BY_PARAM': 'page_size',  # Allow client to override, using `?page_size=xxx`.
    'MAX_PAGINATE_BY': 100 ,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    # 'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.StandardResultsSetPagination'
}



OAUTH2_PROVIDER = {
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
    },
}


AUTHENTICATION_BACKENDS = (
    'oauth2_provider.backends.OAuth2Backend',
    # Uncomment following if you want to access the admin
    # 'django.contrib.auth.backends.ModelBackend',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/tappsi_debug.log',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

USER_AGENTS_CACHE = 'default'

# Nose
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
 
# Lettuce
LETTUCE_SERVER_PORT = 9000

ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = (
        'GET',
        'POST',
        'PUT',
        'PATCH',
        'DELETE',
        'OPTIONS'
    )

SWAGGER_SETTINGS = {
    'api_key':'',
    'info': {
        'contact': 'juniorgerdet@gmail.com',
        'description': 'This is a demo Full API Rest, based on tapsi api and made with'
                       'django rest framework and other libraries, modules, features,'
                       'with the purpose of validate my knowledges.'
                       'My <a href="https://github.com/juniorgerdet"> Git Hub </a>, for open issues, improve...'
                       'For this demo, you can use the api key  "Bearer WpcQH4L8Lf99cuQ2kWwITY8DD9xxM3" to test '
                       'Evaluate through POSTMAN or another Rest Client why this Documentation not support Oauth 2.0'
                       'for tests.',
        'license': 'Apache 2.0',
        'licenseUrl': 'http://www.apache.org/licenses/LICENSE-2.0.html',
        'termsOfServiceUrl': 'http://helloreverb.com/terms/',
        'title': 'Tappsi API Test',
    },
    'token_type':'access_token',
    'doc_expansion': 'none',
}
# http://localhost:8000/api/v1/docs/api-docs
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'tappsi_api/templates'),
) 