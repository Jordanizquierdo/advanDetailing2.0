"""
Django settings for advanDetailing project.

Configuración principal generada por 'django-admin startproject'.
Este archivo contiene todas las configuraciones necesarias para la aplicación Django, 
incluyendo la base de datos, aplicaciones instaladas, middleware y configuración internacional.
"""

from pathlib import Path
import os
import pymysql

# Instalación del conector MySQL para compatibilidad con Django
pymysql.install_as_MySQLdb()

# Definición de la ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta para firmar datos y asegurar la aplicación
SECRET_KEY = 'django-insecure-a34o-s%gihlfb9k$#__f*v$ui3s=ukeps%l2nez9l-9x8mn_9c'

# Indicador de modo de depuración (debe estar deshabilitado en producción)
DEBUG = True

# Hosts permitidos para acceder a la aplicación
ALLOWED_HOSTS = []

# Aplicaciones instaladas en el proyecto
INSTALLED_APPS = [
    'django.contrib.admin',  # Administrador de Django
    'django.contrib.auth',  # Sistema de autenticación
    'django.contrib.contenttypes',  # Tipos de contenido
    'django.contrib.sessions',  # Sesiones
    'django.contrib.messages',  # Mensajería
    'django.contrib.staticfiles',  # Archivos estáticos
    'app1',  # Aplicación personalizada
    'django.contrib.humanize',  # Formateo humanizado de datos
]

# Middleware para gestionar solicitudes y respuestas
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Seguridad adicional
    'django.contrib.sessions.middleware.SessionMiddleware',  # Gestión de sesiones
    'django.middleware.common.CommonMiddleware',  # Funcionalidad común
    'django.middleware.csrf.CsrfViewMiddleware',  # Protección CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Autenticación
    'django.contrib.messages.middleware.MessageMiddleware',  # Gestión de mensajes
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Prevención de clickjacking
]

# Configuración de la raíz de las URL del proyecto
ROOT_URLCONF = 'advanDetailing.urls'

# Configuración de las plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Directorio de plantillas personalizadas
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app1.context_processors.cart_context',  # Procesador de contexto personalizado
            ],
        },
    },
]

# Configuración del servidor WSGI
WSGI_APPLICATION = 'advanDetailing.wsgi.application'

# Configuración de la base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Backend MySQL
        'HOST': 'database-1.c5km2iimkc8x.us-east-2.rds.amazonaws.com',  # Host de la base de datos
        'NAME': 'advan',  # Nombre de la base de datos
        'USER': 'admin',  # Usuario de la base de datos
        'PASSWORD': '967Oa3uxoVkAG4qD4idR',  # Contraseña de la base de datos
        'PORT': '3306',  # Puerto de la base de datos
    }
}

# Configuración de validación de contraseñas
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

# Configuración de logging para registrar errores
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'errors.log',  # Archivo donde se guardan los errores
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Configuración de internacionalización
LANGUAGE_CODE = 'es'  # Idioma predeterminado
TIME_ZONE = 'UTC'  # Zona horaria predeterminada
USE_I18N = True  # Activar traducción de texto
USE_L10N = True  # Activar formateo local de datos
USE_TZ = True  # Activar soporte para zonas horarias

# Configuración de archivos estáticos
STATIC_URL = '/static/'  # URL para acceder a archivos estáticos
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Directorios adicionales de archivos estáticos

# Tipo de clave primaria predeterminado para los modelos
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
