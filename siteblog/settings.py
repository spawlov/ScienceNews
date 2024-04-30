from pathlib import Path

import dj_database_url

from environs import Env

env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", "Fake_Key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", ["127.0.0.1", "localhost"], "[::1]")

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", [])

INTERNAL_IPS = ["127.0.0.1", "localhost"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "ckeditor",
    "ckeditor_uploader",
    "blog.apps.BlogConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "siteblog.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "blog.context_processors.get_general_context",
            ],
        },
    },
]

WSGI_APPLICATION = "siteblog.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(
        default="sqlite:////{0}".format((BASE_DIR / "db.sqlite3"))
    ),
}

# For Postgresql
# DB_URL — postgres://user:password@host:port/db_name
if not DEBUG or DEBUG:
    DB_URL = (
        f"postgres://"
        f"{env('POSTGRES_USER')}:"
        f"{env('POSTGRES_PASSWORD')}@"
        f"{env('POSTGRES_HOST')}:"
        f"{env.int('POSTGRES_PORT')}/"
        f"{env('POSTGRES_DB')}"
    )
    DATABASES = {
        "default": dj_database_url.config(
            default=DB_URL,
            conn_max_age=600,
            conn_health_checks=True,
        ),
    }

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django"
        ".contrib"
        ".auth"
        ".password_validation"
        ".UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django"
        ".contrib"
        ".auth"
        ".password_validation"
        ".MinimumLengthValidator",
    },
    {
        "NAME": "django"
        ".contrib"
        ".auth"
        ".password_validation"
        ".CommonPasswordValidator",
    },
    {
        "NAME": "django"
        ".contrib"
        ".auth"
        ".password_validation"
        ".NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = [BASE_DIR / "blog/static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# SMTP providers
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL = env("EMAIL_MAIL", "")
EMAIL_HOST = "smtp.mail.ru"
EMAIL_PORT = 465
EMAIL_HOST_USER = env("EMAIL_LOGIN_MAIL", "")
EMAIL_HOST_PASSWORD = env("EMAIL_PASSWORD_MAIL", "")
EMAIL_USE_SSL = True
EMAIL_TIMEOUT = 60

ADMINS = (("admin", env("ADMIN_EMAIL", "")),)
EMAIL_SUBJECT_PREFIX = "[SuperService] "
SERVER_EMAIL = EMAIL


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django CKEDITOR
# https://django-ckeditor.readthedocs.io/en/latest/#installation

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_FILENAME_GENERATOR = "blog.utils.get_filename"
CKEDITOR_CONFIGS = {
    "default": {
        "skin": "moono-lisa",
        "toolbar_Basic": [["Source", "-", "Bold", "Italic"]],
        "toolbar_YourCustomToolbarConfig": [
            {
                "name": "document",
                "items": [
                    "Source",
                    "-",
                    "Save",
                    "NewPage",
                    "Preview",
                    "Print",
                    "-",
                    "Templates",
                ],
            },
            {
                "name": "clipboard",
                "items": [
                    "Cut",
                    "Copy",
                    "Paste",
                    "PasteText",
                    "PasteFromWord",
                    "-",
                    "Undo",
                    "Redo",
                ],
            },
            {
                "name": "editing",
                "items": [
                    "Find",
                    "Replace",
                    "-",
                    "SelectAll",
                ],
            },
            {
                "name": "forms",
                "items": [
                    "Form",
                    "Checkbox",
                    "Radio",
                    "TextField",
                    "Textarea",
                    "Select",
                    "Button",
                    "ImageButton",
                    "HiddenField",
                ],
            },
            "/",
            {
                "name": "basicstyles",
                "items": [
                    "Bold",
                    "Italic",
                    "Underline",
                    "Strike",
                    "Subscript",
                    "Superscript",
                    "-",
                    "RemoveFormat",
                ],
            },
            {
                "name": "paragraph",
                "items": [
                    "NumberedList",
                    "BulletedList",
                    "-",
                    "Outdent",
                    "Indent",
                    "-",
                    "Blockquote",
                    "CreateDiv",
                    "-",
                    "JustifyLeft",
                    "JustifyCenter",
                    "JustifyRight",
                    "JustifyBlock",
                    "-",
                    "BidiLtr",
                    "BidiRtl",
                    "Language",
                ],
            },
            {"name": "links", "items": ["Link", "Unlink", "Anchor"]},
            {
                "name": "insert",
                "items": [
                    "Image",
                    "Flash",
                    "Table",
                    "HorizontalRule",
                    "Smiley",
                    "SpecialChar",
                    "PageBreak",
                    "Iframe",
                ],
            },
            "/",
            {
                "name": "styles",
                "items": [
                    "Styles",
                    "Format",
                    "Font",
                    "FontSize",
                ],
            },
            {
                "name": "colors",
                "items": [
                    "TextColor",
                    "BGColor",
                ],
            },
            {
                "name": "tools",
                "items": [
                    "Maximize",
                    "ShowBlocks",
                ],
            },
            {"name": "about", "items": ["About"]},
            "/",
            {
                "name": "yourcustomtools",
                "items": [
                    "Preview",
                    "Maximize",
                ],
            },
        ],
        "toolbar": "YourCustomToolbarConfig",
        "tabSpaces": 4,
        "extraPlugins": ",".join(
            [
                "uploadimage",
                "div",
                "autolink",
                "autoembed",
                "embedsemantic",
                "autogrow",
                "widget",
                "lineutils",
                "clipboard",
                "dialog",
                "dialogui",
                "elementspath",
            ]
        ),
    }
}

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "con_deb": {
            "format": "%(levelname)s :: %(asctime)s :: %(message)s",
        },
        "con_info": {
            "format": "%(levelname)s :: "
            "%(asctime)s :: "
            "%(module)s :: "
            "%(message)s"
        },
        "con_warning": {
            "format": "%(levelname)s :: "
            "%(asctime)s :: "
            "%(message)s :: "
            "%(pathname)s"
        },
        "con_error_cr": {
            "format": "%(levelname)s :: "
            "%(asctime)s :: "
            "%(message)s ::"
            " %(pathname)s :: "
            "%(exc_info)s"
        },
        "file_info_format": {
            "format": "%(levelname)s :: "
            "%(asctime)s :: "
            "%(module)s :: "
            "%(message)s"
        },
        "file_error_format": {
            "format": "%(levelname)s::"
            "%(asctime)s :: "
            "%(message)s :: "
            "%(pathname)s :: "
            "%(exc_info)s"
        },
        "security": {
            "format": "%(levelname)s :: "
            "%(asctime)s :: "
            "%(module)s :: "
            "%(message)s",
        },
        "mail": {
            "format": "%(levelname)s :: "
            "%(asctime)s :: "
            "%(message)s :: "
            "%(pathname)s",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "handlers": {
        "console_debug": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "rich.logging.RichHandler",
            "formatter": "con_deb",
        },
        "console_info": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "rich.logging.RichHandler",
            "formatter": "con_info",
        },
        "console_warning": {
            "level": "WARNING",
            "class": "rich.logging.RichHandler",
            "formatter": "con_warning",
        },
        "console_error": {
            "level": "ERROR",
            "class": "rich.logging.RichHandler",
            "formatter": "con_error_cr",
        },
        "file_info": {
            "level": "INFO",
            "filters": ["require_debug_false"],
            "class": "logging.FileHandler",
            "formatter": "file_info_format",
            "filename": "general.log",
        },
        "file_error": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "formatter": "file_error_format",
            "filename": "error.log",
        },
        "file_security": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "security",
            "filename": "security.log",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
            "formatter": "mail",
        },
    },
    "loggers": {
        "django": {
            "handlers": [
                "console_info",
                "console_warning",
                "console_error",
                "file_info",
            ],
            "level": "INFO",
            "propagate": True,
        },
        "django.request": {
            "handlers": [
                "console_error",
                "mail_admins",
                "file_error",
            ],
            "level": "ERROR",
            "propagate": False,
        },
        "django.server": {
            "handlers": [
                "console_debug",
                "console_info",
                "console_warning",
                "console_error",
                "mail_admins",
                "file_error",
            ],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.template": {
            "handlers": [
                "console_error",
                "mail_admins",
                "file_error",
            ],
            "level": "ERROR",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": [
                "console_error",
                "mail_admins",
                "file_error",
            ],
            "level": "ERROR",
            "propagate": False,
        },
        "django.security": {
            "handlers": [
                "console_info",
                "console_warning",
                "console_error",
                "mail_admins",
                "file_security",
            ],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# Celery Configuration Options
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Cache with Redis on product
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "db": 1,
        },
    },
}
