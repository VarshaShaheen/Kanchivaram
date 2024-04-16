import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = '.env'
load_dotenv(dotenv_path)

SECRET_KEY = 'django-insecure--8a0ejfz-#y_ctr1+#7nh2d3^&psp_o&bo^9e@pkuv0$^vz)fu'

DEBUG = True

ALLOWED_HOSTS = [
    "139.59.79.110",
    'localhost',
    'kanchivaram.radr.in',
    '127.0.0.1',
]

CSRF_TRUSTED_ORIGINS = [
    "http://139.59.79.110:9001",
    "https://localhost:9001",
    'https://kanchivaram.radr.in',
    'http://kanchivaram.radr.in'
]

CORS_ORIGIN_WHITELIST = [
    "http://139.59.79.110:9001",
    "https://localhost:9001",
    'https://kanchivaram.radr.in',
    'http://kanchivaram.radr.in'
]
CORS_ORIGIN_ALLOW_ALL = False

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'payment'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Kanchivaram.urls'

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

WSGI_APPLICATION = 'Kanchivaram.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_ROOT = "app/static/"

STATIC_URL = '/static/'


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PAYMENT_KEY = os.getenv('PAYMENT_KEY')

ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
