import os

logging_level = (
    "INFO" if "LOGGING_LEVEL" not in os.environ else os.environ["LOGGING_LEVEL"]
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "[%(levelname)s]@%(filename)s:%(lineno)s-> %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
        "propagate": False,
    },
    "loggers": {
        "django.server": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "backend": {
            "level": logging_level,
            "handlers": ["console"],
            "propagate": False,
        },
    },
}
