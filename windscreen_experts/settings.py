import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    """Read a true/false env var, accepting True/true/1/yes/on (whitespace ignored)."""
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in ('1', 'true', 'yes', 'on')


SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'  # kept strict on purpose
ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1', '.vercel.app']
CSRF_TRUSTED_ORIGINS = [
    'https://windscreen-experts.vercel.app',
    'https://*.vercel.app',
] + [o for o in os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',') if o]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.core',
    'apps.bookings',
    'apps.gallery',
    'apps.services',
    'apps.inquiries',
]

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

ROOT_URLCONF = 'windscreen_experts.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'windscreen_experts.wsgi.application'

DATABASES = {
    'default': dj_database_url.parse(
        # A blank DATABASE_URL falls back to the local SQLite file instead of breaking
        os.environ.get('DATABASE_URL', '').strip() or f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        # Serverless: don't hold connections between invocations
        conn_max_age=0,
    )
}
if DATABASES['default'].get('ENGINE') == 'django.db.backends.postgresql':
    # Fail fast instead of hanging until Vercel kills the function
    DATABASES['default'].setdefault('OPTIONS', {})
    DATABASES['default']['OPTIONS'].setdefault('connect_timeout', 10)
    DATABASES['default']['OPTIONS'].setdefault('sslmode', 'require')
    # Supabase transaction pooler (port 6543) does not support server-side cursors
    DATABASES['default']['DISABLE_SERVER_SIDE_CURSORS'] = True

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Harare'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Media / File Storage
# Vercel's filesystem is read-only, so uploads must go to object storage in production.
if env_bool('USE_BACKBLAZE'):
    # Backblaze B2 via its S3-compatible API. B2_ENDPOINT_URL may be given with or
    # without https://, e.g. s3.us-east-005.backblazeb2.com
    _b2_host = os.environ.get('B2_ENDPOINT_URL', '').strip().replace('https://', '').replace('http://', '').strip('/')
    DEFAULT_FILE_STORAGE    = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID       = os.environ.get('B2_KEY_ID', '').strip()
    AWS_SECRET_ACCESS_KEY   = os.environ.get('B2_APPLICATION_KEY', '').strip()
    AWS_STORAGE_BUCKET_NAME = os.environ.get('B2_BUCKET_NAME', '').strip()
    AWS_S3_ENDPOINT_URL     = f'https://{_b2_host}'
    AWS_S3_REGION_NAME      = _b2_host.split('.')[1] if _b2_host.count('.') >= 2 else None  # us-east-005
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_DEFAULT_ACL         = None   # B2 visibility is set on the bucket (must be Public)
    AWS_QUERYSTRING_AUTH    = False
    AWS_S3_FILE_OVERWRITE   = False
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'public, max-age=86400'}
    AWS_S3_CUSTOM_DOMAIN    = f'{AWS_STORAGE_BUCKET_NAME}.{_b2_host}'
    MEDIA_URL               = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
elif env_bool('USE_SUPABASE_STORAGE'):
    SUPABASE_PROJECT_ID = os.environ.get('SUPABASE_PROJECT_ID', 'dclubpjyohcduympiskl')
    DEFAULT_FILE_STORAGE  = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID     = os.environ.get('SUPABASE_STORAGE_KEY')
    AWS_SECRET_ACCESS_KEY = os.environ.get('SUPABASE_STORAGE_SECRET')
    AWS_STORAGE_BUCKET_NAME = 'media'
    AWS_S3_ENDPOINT_URL   = f'https://{SUPABASE_PROJECT_ID}.supabase.co/storage/v1/s3'
    AWS_S3_REGION_NAME    = 'us-east-1'
    AWS_DEFAULT_ACL       = 'public-read'
    AWS_QUERYSTRING_AUTH  = False
    AWS_S3_FILE_OVERWRITE = False
    AWS_S3_CUSTOM_DOMAIN  = f'{SUPABASE_PROJECT_ID}.supabase.co/storage/v1/object/public/media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
else:
    MEDIA_URL  = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

# Email - Gmail SMTP
EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_PORT          = 587
EMAIL_USE_TLS       = True
EMAIL_HOST_USER     = os.environ.get('EMAIL_HOST_USER', 'munashe@windowscreens.co.zw')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL  = EMAIL_HOST_USER
ADMIN_EMAIL         = os.environ.get('ADMIN_EMAIL', 'munashe@windowscreens.co.zw')
# Never let a slow/blocked SMTP server hang a request
EMAIL_TIMEOUT       = 10
if not EMAIL_HOST_PASSWORD:
    # No SMTP credentials configured: log emails instead of trying to send
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Google Analytics
GA_MEASUREMENT_ID = os.environ.get('GA_MEASUREMENT_ID', '')

# Auth
LOGIN_URL          = '/admin-panel/login/'
LOGIN_REDIRECT_URL = '/admin-panel/'
