# -*- coding: utf-8 -*-
# Django settings for shotApp project.

"""
Author  : Anshul Tiwari
Date    : Sep 30, 2015

Description : This holds the settings.
"""


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

import os
FILE_PATH = os.path.realpath(os.path.dirname(__file__))

MANAGERS = ADMINS

import socket


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'cleanup_portal',                      # Or path to database file if using sqlite3.
        'USER': 'cleanup',                      # Not used with sqlite3.
        'PASSWORD': 'cleanup-password',                  # Not used with sqlite3.
        'HOST': '172.16.15.246',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5555',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1
BASE_URL = '/'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
# MEDIA_ROOT = ''
MEDIA_ROOT = '%s/media' % FILE_PATH

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
# MEDIA_URL = ''
MEDIA_URL = '/site-media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

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
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '1as_eze(y0yq0&l6aqnpvf8)7@i3j&^pq3&h3ef84l^)wt+2l('

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'AssetMan.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '%s/templates' % FILE_PATH,
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rpc',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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

LDAP_HOST       = 'ldap://ldap.local'

# Override default authentication system.
#
# 'django.contrib.auth.backends.ModelBackend'
# Must be present otherwise ctac cannot get user group information.
# This allows ctac to get the groups users are assigned to from the django authentication
# system as well as allow users to login with a django password.  
# ie. the default password specified above.
# This allows for users to login without authenticating again the LDAP server if it is down
# or allow admins to login to debug/test user accounts.
AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

try:
    import ldap
    from django_auth_ldap.config import LDAPSearch
except ImportError:
    pass
    pass
else:
    AUTH_LDAP_SERVER_URI = 'ldap://ldap.local'
    AUTH_LDAP_BIND_DN = ""
    AUTH_LDAP_BIND_PASSWORD = ""
    AUTH_LDAP_USER_SEARCH = LDAPSearch("dc=, dc=COM", ldap.SCOPE_SUBTREE, "(sAMACcountName=%(user)s)")

    # Populate the Django user information from the LDAP information
    AUTH_LDAP_USER_ATTR_MAP = {
        'first_name': "givenName", 
        "last_name": "sn", 
        "email": "mail"
    }

# User object will be updated with the latest values from the LDAP directory at every login
AUTH_LDAP_ALWAYS_UPDATE_USER = True

