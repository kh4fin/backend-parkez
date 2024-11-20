from pathlib import Path
from decouple import config 
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # corsheader
    "corsheaders",
	# rest-framework
    'rest_framework',
    'rest_framework.authtoken',
	# dj-rest-auth
	'dj_rest_auth.registration',
    'dj_rest_auth',
	# allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
	# allauth social accounts
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # local app
    "accounts",
    "parking",
    # email brevo
    'anymail',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # cors header middleware
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware"
]

ROOT_URLCONF = 'backend_site.urls'

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

WSGI_APPLICATION = 'backend_site.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',  
#         'USER': 'postgres.ktyeokijfsdecgazqlvv',  
#         'PASSWORD': 'YOUR-PASSWORD',  
#         'HOST': 'aws-0-ap-southeast-1.pooler.supabase.com',  
#         'PORT': '6543', 
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')



# allauth
SITE_ID = 1
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]


# rest-framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# simple jwt
from datetime import timedelta
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# rest auth
REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'access',
    'JWT_AUTH_REFRESH_COOKIE': 'refresh',
    'JWT_AUTH_HTTPONLY': True,
    'SESSION_LOGIN': False,
    'OLD_PASSWORD_FIELD_ENABLED': True,
}




# cors headers
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "https://parkez-app.vercel.app",
    "http://localhost:5173",
]

# ANYMAIL = {
#     "BREVO_API_KEY": "key",  
# }

# EMAIL_BACKEND = "anymail.backends.brevo.BrevoBackend" 
# DEFAULT_FROM_EMAIL = 

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp-relay.brevo.com'  
# EMAIL_PORT = 587  
# EMAIL_USE_TLS = True  
# EMAIL_HOST_USER = '7fefa2001@smtp-brevo.com'  
# EMAIL_HOST_PASSWORD = 'TpdbwCnHKS4kI6G2'  
# DEFAULT_FROM_EMAIL = '7fefa2001@smtp-brevo.com' 



# send email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_HOST_USER = '9e9519719d8a78'
EMAIL_HOST_PASSWORD = '01a66fad551b6f'
EMAIL_PORT = '2525'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'webmaster@localhost'
AUTH_USER_MODEL = "accounts.CustomUserModel"






# REST_AUTH_REGISTER_SERIALIZERS = {
#     'REGISTER_SERIALIZER': 'accounts.serializers.CustomRegisterSerializer',
# }

# SITE_ID = 1
# ACCOUNT_USER_MODEL_USERNAME_FIELD = None  
# ACCOUNT_USERNAME_REQUIRED = False  
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  


# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
#         'rest_framework.authentication.SessionAuthentication',
#         'rest_framework.authentication.TokenAuthentication',
#     ],
# }

# from datetime import timedelta

# # simple jwt
# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),  
#     'REFRESH_TOKEN_LIFETIME': timedelta(hours=2), 
# }

# REST_AUTH_REGISTER_SERIALIZERS = {
#     'REGISTER_SERIALIZER': 'accounts.serializers.CustomRegisterSerializer',
# }



# # rest auth
# REST_AUTH = {
#     'USE_JWT': True,
#     'JWT_AUTH_COOKIE': 'access',
#     'JWT_AUTH_REFRESH_COOKIE': 'refresh',
#     'JWT_AUTH_HTTPONLY': False,
#     'SESSION_LOGIN': False,
#     'OLD_PASSWORD_FIELD_ENABLED': True,
# }


# # cors headers
# CORS_ALLOW_CREDENTIALS = True

# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5173" 
# ]

# CSRF_COOKIE_SECURE = False     
# SESSION_COOKIE_SECURE = False 


