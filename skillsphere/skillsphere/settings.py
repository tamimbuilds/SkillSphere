import os
from pathlib import Path
from urllib.parse import quote, urlparse

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-dev-only-key')

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'


def _normalize_host(value):
    value = (value or '').strip()
    if not value:
        return ''

    if '://' in value:
        parsed = urlparse(value)
        return parsed.hostname or ''

    # Drop any path or port from accidentally pasted host values.
    value = value.split('/')[0].strip()
    if ':' in value and value.count(':') == 1:
        value = value.split(':', 1)[0].strip()
    return value

allowed_hosts = [
    '127.0.0.1',
    'localhost',
    'healthcheck.railway.app',
    '.up.railway.app',
]
allowed_hosts.extend(
    host
    for host in (_normalize_host(item) for item in os.getenv('ALLOWED_HOSTS', '').split(','))
    if host
)

railway_public_domain = _normalize_host(os.getenv('RAILWAY_PUBLIC_DOMAIN', ''))
if railway_public_domain:
    allowed_hosts.append(railway_public_domain)

ALLOWED_HOSTS = allowed_hosts

csrf_trusted_origins = [
    origin.strip()
    for origin in os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',')
    if origin.strip()
]
if railway_public_domain:
    csrf_trusted_origins.append(f'https://{railway_public_domain}')

CSRF_TRUSTED_ORIGINS = csrf_trusted_origins



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'interviews',  
    'jobs',        
    'skills',
]

AUTH_USER_MODEL = 'accounts.User'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'skillsphere.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'skillsphere.wsgi.application'


def _build_postgres_url():
    pg_name = os.getenv('PGDATABASE') or os.getenv('POSTGRES_DB')
    pg_user = os.getenv('PGUSER') or os.getenv('POSTGRES_USER')
    pg_password = os.getenv('PGPASSWORD') or os.getenv('POSTGRES_PASSWORD')
    pg_host = os.getenv('PGHOST') or os.getenv('POSTGRES_HOST')
    pg_port = os.getenv('PGPORT') or os.getenv('POSTGRES_PORT') or '5432'

    if all([pg_name, pg_user, pg_password, pg_host]):
        return (
            f"postgresql://{quote(pg_user)}:{quote(pg_password)}"
            f"@{pg_host}:{pg_port}/{pg_name}"
        )
    return None


def _first_env(*names):
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return None


database_url = _first_env('DATABASE_URL', 'DATABASE_PRIVATE_URL', 'POSTGRES_URL', 'POSTGRESQL_URL') or _build_postgres_url()


def _is_collectstatic_command():
    return any(arg == 'collectstatic' for arg in os.sys.argv)


def _is_railway_environment():
    return any(
        os.getenv(name)
        for name in (
            'RAILWAY_ENVIRONMENT_ID',
            'RAILWAY_ENVIRONMENT_NAME',
            'RAILWAY_PROJECT_ID',
            'RAILWAY_SERVICE_ID',
            'RAILWAY_DEPLOYMENT_ID',
        )
    )


allow_sqlite_fallback = DEBUG or _is_collectstatic_command() or not _is_railway_environment()

DATABASES = {
    'default': dj_database_url.parse(database_url, conn_max_age=600) if database_url else (
        {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
        if allow_sqlite_fallback
        else None
    )
}

if DATABASES['default'] is None:
    database_env_names = (
        'DATABASE_URL',
        'DATABASE_PRIVATE_URL',
        'POSTGRES_URL',
        'POSTGRESQL_URL',
        'PGDATABASE',
        'PGUSER',
        'PGPASSWORD',
        'PGHOST',
        'PGPORT',
        'POSTGRES_DB',
        'POSTGRES_USER',
        'POSTGRES_PASSWORD',
        'POSTGRES_HOST',
        'POSTGRES_PORT',
    )
    railway_env_names = (
        'RAILWAY_ENVIRONMENT_ID',
        'RAILWAY_ENVIRONMENT_NAME',
        'RAILWAY_PROJECT_ID',
        'RAILWAY_SERVICE_ID',
        'RAILWAY_SERVICE_NAME',
        'RAILWAY_DEPLOYMENT_ID',
    )
    present_database_env = ', '.join(name for name in database_env_names if os.getenv(name)) or 'none'
    present_railway_env = ', '.join(name for name in railway_env_names if os.getenv(name)) or 'none'
    print(f'Database env vars present: {present_database_env}')
    print(f'Railway env vars present: {present_railway_env}')
    raise ImproperlyConfigured(
        'Database configuration is missing. Set DATABASE_URL on this app service. '
        'On Railway, add DATABASE_URL=${{ Postgres.DATABASE_URL }} to the Django service '
        'Variables tab, replacing "Postgres" with the exact name of your PostgreSQL service. '
        'Alternatively set PGDATABASE, PGUSER, PGPASSWORD, PGHOST, and optionally PGPORT.'
    )


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_REDIRECT_EXEMPT = [r'^health/$']
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
