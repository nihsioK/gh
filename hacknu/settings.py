from pathlib import Path
import os
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-f9)dpxx%bs5e&yl@qvd^9k4not-u-8kepz+tuuamegacg9((uo'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'monkfish-app-nvvs7.ondigitalocean.app'] 


CORS_ALLOWED_ORIGINS = [
    "https://localhost:5173",
    "http://localhost:8080",
    "https://localhost:8080",
    'https://monkfish-app-nvvs7.ondigitalocean.app',
] 

CSRF_ALLOWED_ORIGINS = [
    "https://localhost:5173",
    "http://localhost:8080",
    "https://localhost:8080",
    'https://monkfish-app-nvvs7.ondigitalocean.app',
] 

CSRF_TRUSTED_ORIGINS = [
    "https://localhost:5173",
    "http://localhost:8080",
    "https://localhost:8080",
    'https://monkfish-app-nvvs7.ondigitalocean.app',
] 

CSRF_COOKIE_HTTPONLY = False  
CSRF_COOKIE_SECURE = True   
CSRF_COOKIE_SAMESITE = 'None'  


CORS_ALLOW_CREDENTIALS = True  
SESSION_COOKIE_SAMESITE = 'None' 
SESSION_COOKIE_SECURE = True  


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'sslserver',

    
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    
    'base',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    'corsheaders.middleware.CorsMiddleware', 

    
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hacknu.urls'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'hacknu.wsgi.application'



DATABASES = {
	'default': {  
		'ENGINE': 'django.db.backends.postgresql_psycopg2',  
		'NAME': 'hacknu',
        'USER': 'postgres',
        'PASSWORD': '/Im|+VU5SY&fppCS',
        'HOST': '35.228.223.35',
        'PORT': '5432',
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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = 'static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media') 
MEDIA_URL = '/media/' 



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' 

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=250),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256', #RS256
    'SIGNING_KEY': "oqufhqwuifgqyuqg78o123ert78123rg23i",
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}



# SECURE_SSL_REDIRECT = True  # Redirecting all HTTP requests to HTTPS
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')  # Setting the proxy SSL header