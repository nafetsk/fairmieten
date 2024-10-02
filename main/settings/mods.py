import os
import environ
from .main import INSTALLED_APPS, BASE_DIR


INSTALLED_APPS += ["environ", "fairmieten", "main.hello", "aggregation"]

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


# False if not in os.environ because of casting above
DEBUG = env("DEBUG")

ALLOWED_HOSTS = ["fairmieten.ecord.de", "localhost", "127.0.0.1"]

# Raises Django's ImproperlyConfigured
# exception if SECRET_KEY not in os.environ
SECRET_KEY = env("SECRET_KEY")

STATIC_ROOT = "staticfiles/"


# Parse database connection url strings
# like psql://user:pass@127.0.0.1:8458/db
DATABASES = {
    # read os.environ['DATABASE_URL'] and raises
    # ImproperlyConfigured exception if not found
    "default": env.db_url("DATABASE_URL", default="sqlite:////tmp/my-tmp-sqlite.db")
}
