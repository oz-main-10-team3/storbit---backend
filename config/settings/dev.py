import os

from config.settings.base import *

from .base import *

DEBUG = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

INTERNAL_IPS = [
    "127.0.0.1",
]

ALLOWED_ORIGINS: list[str] = os.getenv("CORS_ALLOWED_ORIGINS", "").split(" ")
