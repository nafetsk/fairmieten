import os
import environ
from django.templatetags.static import static
from .main import INSTALLED_APPS, MIDDLEWARE
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [ "unfold"] + INSTALLED_APPS + [ "environ", "fairmieten", "aggregation", "widget_tweaks"]

MIDDLEWARE += ['django_htmx.middleware.HtmxMiddleware', 'whitenoise.middleware.WhiteNoiseMiddleware', "django.contrib.auth.middleware.LoginRequiredMiddleware"]

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, "data/env_variables", ".env"))


# False if not in os.environ because of casting above
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["fairmieten.ecord.de", "localhost", "127.0.0.1"])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=["https://fairmieten.ecord.de"])
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Raises Django's ImproperlyConfigured
# exception if SECRET_KEY not in os.environ
SECRET_KEY = env("SECRET_KEY")

STATIC_ROOT = "staticfiles/"


LOGIN_URL = "/login/"

# Parse database connection url strings
# like psql://user:pass@127.0.0.1:8458/db


DATABASES = {
    # read os.environ['DATABASE_URL'] and raises
    # ImproperlyConfigured exception if not found
    "default": env.db_url("DATABASE_URL", default="sqlite:///data/database/db.sqlite3"),
}
DATABASES["default"]["OPTIONS"] = env.list("DATABASE_OPTIONS",default={"timeout": 20})
print(DATABASES["default"])

UNFOLD = {
    "SITE_HEADER": "Fairmieten Admin",
     "SITE_ICON": {
        "light": lambda request: static("logo/logo_icon.svg"),  # light mode
        "dark": lambda request: static("icon-dark.svg"),  # dark mode
    },
	"STYLES": [
        lambda request: static("css/unfold_custom.css"),
    ],
     "COLORS": {
        "font": {
            "subtle-light": "107 114 128",
            "subtle-dark": "156 163 175",
            "default-light": "75 85 99",
            "default-dark": "209 213 219",
            "important-light": "17 24 39",
            "important-dark": "243 244 246",
        },
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "79 158 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
}

# Password reset
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')