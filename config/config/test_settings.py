"""테스트 전용 Django 설정 — SQLite 인메모리 DB, AWS 더미값 사용"""
import os

os.environ.setdefault("SECRET_KEY", "test-secret-key-not-for-production")
os.environ.setdefault("DB_NAME", "test_db")
os.environ.setdefault("DB_USER", "test_user")
os.environ.setdefault("DB_PASSWORD", "test_pass")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("AWS_ACCESS_KEY", "fake-access-key")
os.environ.setdefault("AWS_SECRET_KEY", "fake-secret-key")
os.environ.setdefault("AWS_BUCKET", "fake-bucket")
os.environ.setdefault("AWS_STATIC", "ap-northeast-2")

from config.settings import *  # noqa: F401, F403, E402

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
