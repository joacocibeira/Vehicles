from .base import *
import sys


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Define databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(
            BASE_DIR, "db.sqlite3"
        ),  # Path to your default database file
    }
}

if "pytest" in sys.argv:
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "test_db.sqlite3",
    }
