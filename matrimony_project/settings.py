from pathlib import Path
from decouple import config, Csv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-temp-key-for-build-only-123456789'
)
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = [
    "66.116.240.195",
    "srivilliputhur.online",
    "www.srivilliputhur.online",
    "rajapalayammatrimony.com",
    "www.rajapalayammatrimony.com",
    "127.0.0.1",
    "localhost",
]

SITE_URL = config(
    'SITE_URL',
    default='https://rajapalayammatrimony.com'
)

CSRF_TRUSTED_ORIGINS = [
    "http://66.116.240.195",
    "https://66.116.240.195",
    "https://www.rajapalayammatrimony.com",
    "https://rajapalayammatrimony.com",
    "http://www.rajapalayammatrimony.com",   # ← ADD THIS
    "http://rajapalayammatrimony.com",        # ← ADD THIS
    "https://www.srivilliputhur.online",
    "https://srivilliputhur.online",
    "http://srivilliputhur.online",           # ← FIX TYPO (was srivilliputtur)
    "http://www.srivilliputhur.online",       # ← ADD THIS
]
# =============================================
# INSTALLED APPS
# =============================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'cloudinary',
    'cloudinary_storage',
    'csp',

    # Your apps
    'accounts',
    'profiles',
    'matches',
    'search',
    'payments',
    'notifications',
    'dashboard',
]

# =============================================
# MIDDLEWARE
# =============================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'csp.middleware.CSPMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'matrimony_project.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'matrimony_project.wsgi.application'

# =============================================
# DATABASE
# ========================================
DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    try:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.parse(
                DATABASE_URL,
                conn_max_age=600,
            )
        }
    except Exception:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
# =============================================
# PASSWORD VALIDATION
# =============================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =============================================
# INTERNATIONALIZATION
# =============================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# =============================================
# STATIC FILES
# =============================================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = (
    'django.contrib.staticfiles.storage.StaticFilesStorage'
)

# =============================================
# MEDIA FILES
# =============================================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =============================================
# CLOUDINARY
# =============================================
CLOUDINARY_CLOUD_NAME = config(
    'CLOUDINARY_CLOUD_NAME', default=''
)
CLOUDINARY_API_KEY = config(
    'CLOUDINARY_API_KEY', default=''
)
CLOUDINARY_API_SECRET = config(
    'CLOUDINARY_API_SECRET', default=''
)

if CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY:
    try:
        import cloudinary
        import cloudinary.uploader
        import cloudinary.api

        cloudinary.config(
            cloud_name=CLOUDINARY_CLOUD_NAME,
            api_key=CLOUDINARY_API_KEY,
            api_secret=CLOUDINARY_API_SECRET,
            secure=True
        )
        CLOUDINARY_STORAGE = {
            'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,
            'API_KEY': CLOUDINARY_API_KEY,
            'API_SECRET': CLOUDINARY_API_SECRET,
        }
        DEFAULT_FILE_STORAGE = (
            'cloudinary_storage.storage'
            '.MediaCloudinaryStorage'
        )
        MEDIA_URL = '/media/'
        print('✅ Cloudinary configured')
    except Exception as e:
        print(f'Cloudinary error: {e}')
        DEFAULT_FILE_STORAGE = (
            'django.core.files.storage.FileSystemStorage'
        )
        MEDIA_URL = '/media/'
        MEDIA_ROOT = BASE_DIR / 'media'
else:
    DEFAULT_FILE_STORAGE = (
        'django.core.files.storage.FileSystemStorage'
    )
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

# =============================================
# AUTH
# =============================================
AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

EMAIL_HOST_USER = 'admin.matrimonyinfo@gmail.com'
EMAIL_HOST_PASSWORD = 'ziffjurffpxmbnge'

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_TIMEOUT = 30

# =============================================
# PAYMENT
# =============================================
CASHFREE_APP_ID = config('CASHFREE_APP_ID', default='')
CASHFREE_SECRET_KEY = config('CASHFREE_SECRET_KEY', default='')
CASHFREE_ENV = config('CASHFREE_ENV', default='TEST')

# =============================================
# CONTENT SECURITY POLICY (Cashfree checkout)
# =============================================
CSP_DEFAULT_SRC = ("'self'",)

CSP_SCRIPT_SRC = (
    "'self'",
    "'unsafe-inline'",
    "'unsafe-eval'",
    "https://cdn.jsdelivr.net",
    "https://cdnjs.cloudflare.com",
    "https://sdk.cashfree.com",
    "https://*.cashfree.com",
)
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
    "https://cdn.jsdelivr.net",
    "https://cdnjs.cloudflare.com",
    "https://fonts.googleapis.com",
    "https://*.cashfree.com",
)
CSP_FONT_SRC = (
    "'self'",
    "https://cdn.jsdelivr.net",
    "https://cdnjs.cloudflare.com",
    "https://fonts.gstatic.com",
)
CSP_CONNECT_SRC = (
    "'self'",
    "https://cdn.jsdelivr.net",
    "https://cdnjs.cloudflare.com",
    "https://*.cashfree.com",
    "https://api.cashfree.com",
    "https://sandbox.cashfree.com",
)
CSP_FRAME_SRC = (
    "'self'",
    "https://*.cashfree.com",
    "https://sandbox.cashfree.com",
)
CSP_IMG_SRC = ("'self'", "data:", "https:")

# =============================================
# SECURITY (Production)
# =============================================

if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'SAMEORIGIN'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_SAMESITE = 'Lax'        # ← ADD THIS
    SESSION_COOKIE_SAMESITE = 'Lax'     # ← ADD THIS
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')  # ← ADD THIS

# =============================================
# MESSAGES
# =============================================
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# =============================================
# DEFAULT PRIMARY KEY
# =============================================
DEFAULT_AUTO_KEY_FIELD = 'django.db.models.BigAutoField'

# =============================================
# PASSWORD RESET
# =============================================
PASSWORD_RESET_TIMEOUT = 86400

# Speed optimizations
# Speed
CONN_MAX_AGE = 60
WHITENOISE_MAX_AGE = 31536000

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

# =============================================
# FIREBASE INITIALIZATION
# =============================================

try:
    from .firebase_service import *
except Exception as e:
    print(f"Firebase initialization failed: {e}")



# Path to your firebase_key.json (already in your project root)
FIREBASE_KEY_PATH = os.path.join(BASE_DIR, 'firebase_key.json')