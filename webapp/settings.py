"""
Django settings for webapp project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rkn*kar688t+b^ch(gd1x$9zb@679yzk6rnq5fwun@41tw8&7m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Social Django needed for Globus Auth
    'social_django.middleware.SocialAuthExceptionMiddleware',
    # The middleware handles all globus related authentication exceptions.
    # Uncomment if using Globus sessions or/and Globus groups.
    # 'webapp.middleware.GlobusAuthExceptionMiddleware',
]

ROOT_URLCONF = 'webapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'webapp.wsgi.application'

AUTHENTICATION_BACKENDS = [
    'webapp.globus.GlobusOpenIdConnect',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_GLOBUS_KEY = ''
SOCIAL_AUTH_GLOBUS_SECRET = ''
SOCIAL_AUTH_GLOBUS_AUTH_EXTRA_ARGUMENTS = {
    'access_type': 'offline',
}
SOCIAL_AUTH_GLOBUS_SCOPE = [
    'urn:globus:auth:scope:nexus.api.globus.org:groups',
    'urn:globus:auth:scope:search.api.globus.org:search',
    # Add the group scope to be able to verify if a user is a member of a Globus
    # group. To use the group scope, your Globus Auth Client ID has to be
    # whitelisted. Please contact support@globus.org to whitelist your Client ID.
    # 'urn:globus:auth:scope:nexus.api.globus.org:groups',
]
# Set to True to retrieve information about a user identity from the Globus
# sessions instead of relying on a Globus OIDC userinfo endpoint.
# SOCIAL_AUTH_GLOBUS_SESSIONS = False

# Set to a UUID of a Globus group if you want to restrict access to the portal
# to members of the Globus group. You will also have to add the group scope
# urn:globus:auth:scope:nexus.api.globus.org:groups to SOCIAL_AUTH_GLOBUS_SCOPE.
# SOCIAL_AUTH_GLOBUS_ALLOWED_GROUP = '<Globus_group_UUID>'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
