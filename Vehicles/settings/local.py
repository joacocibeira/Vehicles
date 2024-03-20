from .base import *


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Define databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(
            BASE_DIR, "db.sqlite3"
        ),  # Path to your default database file
    },
    "test": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(
            BASE_DIR, "test_db.sqlite3"
        ),  # Path to your test database file
    },
}
