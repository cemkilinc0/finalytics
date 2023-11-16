"""
Django settings for router project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from typing import List
from decouple import config
import structlog


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")  #

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS: List[str]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "financial_data_engine",
    "analysis_engine",
    "django_extensions",
    "django_celery_beat",
    "django_celery_results",
    "django_redis",
    "debug_toolbar",
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

INTERNAL_IPS = [
    "127.0.0.1",  # Debug Toolbar will only be accessible from your local machine
]

ROOT_URLCONF = "router.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "router.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "finalytics_db",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "db",
        "PORT": "5432",
    }
}

""" django debug toolbar """
if DEBUG:
    # remove when in production!
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda r: True,
    }

""""""

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


""" Logging """

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "structlog": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(colors=True),
            "foreign_pre_chain": [],
        },
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console_structlog": {
            "class": "logging.StreamHandler",
            "formatter": "structlog",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join("logs", "debug.log"),
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console", "mail_admins", "console_structlog"],
            "level": "WARNING",
            "propagate": True,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "": {
            "handlers": ["file", "console", "mail_admins", "console_structlog"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.ExceptionPrettyPrinter(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)


""" Celery """

CELERY_BROKER_URL = "redis://redis:6379/0"
REDBEAT_REDIS_URL = "redis://redis:6379/0"
REDIS_LOCK_URL = "redis://redis:6379/2"
CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_EXPIRES = 43200  # 12 hours

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

CELERY_REDBEAT_SCHEDULE_KEY = "redbeat::schedule"


SHELL_PLUS_PRE_IMPORTS = [
    # Models
    ("financial_data_engine.models.balance_sheet_statement", "BalanceSheetTableModel"),
    ("financial_data_engine.models.cashflow_statement", "CashFlowTableModel"),
    ("financial_data_engine.models.company", "CompanyTableModel"),
    ("financial_data_engine.models.income_statement", "IncomeStatementTableModel"),
    ("financial_data_engine.models.key_metrics", "KeyMetricsTableModel"),
    # Services
    ("financial_data_engine.services.balance_sheet_service", "BalanceSheetService"),
    ("financial_data_engine.services.cashflow_service", "CashflowService"),
    ("financial_data_engine.services.company_service", "CompanyService"),
    ("financial_data_engine.services.income_statement_service", "IncomeStatementService"),
    ("financial_data_engine.services.key_metrics_service", "KeyMetricsService"),
    ("analysis_engine.agents.income_statement_agent", "IncomeStatementAnalysisAgent"),
    # Gateways
    ("financial_data_engine.gateway.fmp_gateway", "FinancialModelingPrepGateway"),
    # Lib
    ("financial_data_engine.lib.repository", "Repository"),
    # Views
    ("financial_data_engine.views.balance_sheet_view", "BalanceSheetView"),
    ("financial_data_engine.views.cashflow_view", "CashflowView"),
    ("financial_data_engine.views.company_query_view", "CompanyQueryView"),
    ("financial_data_engine.views.income_statement_view", "IncomeStatementView"),
    ("financial_data_engine.views.key_metrics_view", "KeyMetricsView"),
]
