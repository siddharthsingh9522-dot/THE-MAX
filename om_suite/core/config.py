"""App configuration — everything comes from environment variables (see .env.example)."""
import os
import secrets
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def _flag(name: str, default: bool = False) -> bool:
    v = os.environ.get(name)
    if v is None:
        return default
    return v.strip().lower() in ("1", "true", "yes", "on")


def _csv(name: str) -> set:
    return {x.strip().lower() for x in os.environ.get(name, "").split(",") if x.strip()}


class Config:
    APP_NAME = os.environ.get("APP_NAME", "OM Suite")
    APP_VERSION = "1.0.0-phase1"

    ENV = os.environ.get("APP_ENV", os.environ.get("FLASK_ENV", "development")).lower()
    IS_PROD = ENV == "production"

    SECRET_KEY = os.environ.get("SECRET_KEY") or ""
    if not SECRET_KEY:
        if IS_PROD:
            raise RuntimeError("SECRET_KEY environment variable is required in production.")
        SECRET_KEY = "dev-" + secrets.token_hex(16)  # dev only: sessions reset on restart

    # --- sessions / cookies ---
    PERMANENT_SESSION_LIFETIME = timedelta(days=int(os.environ.get("SESSION_DAYS", "14")))
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = IS_PROD
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_UPLOAD_MB", "50")) * 1024 * 1024
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(days=7)

    # --- users / admin ---
    # Emails listed here become approved admins the moment they sign up.
    # If this is empty, the very first signup becomes the admin (local/dev convenience).
    ADMIN_EMAILS = _csv("ADMIN_EMAILS")
    USER_CACHE_TTL = int(os.environ.get("USER_CACHE_TTL", "10"))  # seconds

    # --- storage: Firebase Firestore (recommended) or local SQLite fallback ---
    FIREBASE_PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID", "ptp-report")
    FIREBASE_SERVICE_ACCOUNT_JSON = os.environ.get("FIREBASE_SERVICE_ACCOUNT_JSON", "")
    FIREBASE_SERVICE_ACCOUNT_FILE = os.environ.get("FIREBASE_SERVICE_ACCOUNT_FILE", "")
    FIRESTORE_PREFIX = os.environ.get("FIRESTORE_PREFIX", "omsuite_")
    DATA_DIR = Path(os.environ.get("DATA_DIR", str(BASE_DIR / "data")))

    # --- links to other deployments ---
    GR_AUTO_URL = os.environ.get("GR_AUTO_URL", "").strip()

    TRUST_PROXY = _flag("TRUST_PROXY", IS_PROD)
    DISPLAY_TZ_OFFSET_MIN = int(os.environ.get("DISPLAY_TZ_OFFSET_MIN", "330"))  # IST
