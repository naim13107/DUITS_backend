
from pathlib import Path
from decouple import config 
from datetime import timedelta

FRONTEND_ALLOW = config('FRONTEND_ALLOW',default = '*')
BACKEND_ALLOW = config('BACKEND_ALLOW',default = '*')

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')


DEBUG = config('DEBUG',default = False)

ALLOWED_HOSTS = [BACKEND_ALLOW, FRONTEND_ALLOW , 'duits-backend.vercel.app', 'duits-frontend.vercel.app']
AUTH_USER_MODEL = 'users.User'



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'djoser',
    'drf_yasg',
    'users',
    'article',
    'recruitment',
    'panel',
    'event',
    'gallery',
    'contact',
    'analytics',
    'payment',
    'notice',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'duits_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        
        # UPDATE THIS LINE:
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

WSGI_APPLICATION = 'duits_backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DBNAME'),
        'USER': config('DBUSER'),
        'PASSWORD': config('DBPASS'),
        'HOST': config('HOST'),
        'PORT': config('DBBPORT'),
    }
}



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

SIMPLE_JWT = {
   'AUTH_HEADER_TYPES': ('JWT',),
   "ACCESS_TOKEN_LIFETIME": timedelta(days=5),
}



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

FRONTEND_BASE_URL = config('FRONTEND_BASE_URL')
BACKEND_BASE_URL = config('BACKEND_BASE_URL')

CORS_ALLOWED_ORIGINS = [
    BACKEND_BASE_URL, 
    FRONTEND_BASE_URL, 
   
]

CORS_ALLOW_CREDENTIALS = True



STATIC_URL = 'static/'

import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ==========================================
# DJOSER CONFIGURATION
# ==========================================
DJOSER = {
    'SERIALIZERS': {
        'user': 'users.serializers.CustomUserSerializer',
        'current_user': 'users.serializers.CustomUserSerializer',
    },
    
    'LOGIN_FIELD': 'email',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'TOKEN_MODEL': None, 
    
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    
   
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'PASSWORD_RESET_CONFIRM_URL': 'password-reset/{uid}/{token}',
}


DOMAIN = config('DOMAIN')  
SITE_NAME = 'Dhaka University IT Society'

SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {
      'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description' : 'Enter your JWT token in the format : `JWT` <your_token>'

      }
   }
}

REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

# ==========================================
# EMAIL SETTINGS
# ==========================================
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)

# ⚠️ Replace these with your actual Gmail details
# Note: Use an "App Password" (16 characters), NOT your normal Gmail password!
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')  # Store this in your .env file for security!
EMAIL_HOST_PASSWORD = config('APPPASS', default='')  # Store this in your .env file for security!
DEFAULT_FROM_EMAIL = 'DUITS Admin <duits.lab@gmail.com>'

AAMARPAY_BASE_URL=config('AAMARPAY_BASE_URL')
AAMARPAY_STORE_ID=config('AAMARPAY_STORE_ID')
AAMARPAY_SIGNATURE_KEY=config('AAMARPAY_SIGNATURE_KEY')