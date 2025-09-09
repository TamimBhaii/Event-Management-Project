"""
Django settings for event_management_system project.
"""

from pathlib import Path
import dj_database_url
# -----------------------
# BASE DIRECTORY
# -----------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------
# SECURITY
# -----------------------
SECRET_KEY = 'django-insecure-uq!i2kx3u5)32lcp=a3c6#7g$l^wcq@0&cn^lk782n1czgmd&x'
DEBUG = True
ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    "https://event-management-system-project-y7iq.onrender.com",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]


# -----------------------
# INSTALLED APPS
# -----------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize', 
    'system',      
                 
]

# -----------------------
# MIDDLEWARE
# -----------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -----------------------
# URL & WSGI
# -----------------------
ROOT_URLCONF = 'event_management_system.urls'

WSGI_APPLICATION = 'event_management_system.wsgi.application'

# -----------------------
# TEMPLATES
# -----------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'system' / 'templates'],  # project-level templates
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

# -----------------------
# DATABASE (PostgreSQL)
# -----------------------
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'event_management_db',
#         'USER': 'postgres',
#         'PASSWORD': '123456789',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }



DATABASES = {
    'default': dj_database_url.config(
        # Replace this value with your local database's connection string.
        default='postgresql://event_manager_db_wapc_user:tE3sfAcVZtUkK2pfdQypatU07of2Inh4@dpg-d309u1h5pdvs73aqfi0g-a.oregon-postgres.render.com/event_manager_db_wapc',
        conn_max_age=600
    )
}


# -----------------------
# AUTH PASSWORD VALIDATORS
# -----------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# -----------------------
# INTERNATIONALIZATION
# -----------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# -----------------------
# STATIC FILES (CSS, JS, Tailwind)
# -----------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'system' / 'static'  # points to your system/static folder
]

# -----------------------
# MEDIA FILES (Images, Uploads)
# -----------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # uploaded images will go here

# -----------------------
# DEFAULT AUTO FIELD
# -----------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
