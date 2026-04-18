# enter your overrides here
from pathlib import Path

BACKUP_HOME_DIR = Path("/data/backups")
BACKUP_BORG_DIR = BACKUP_HOME_DIR / "borg"
BACKUP_AUTHORIZED_KEYS = BACKUP_HOME_DIR / ".ssh" / "authorized_keys"
BACKUP_USER = "borg"
BACKUP_REPO_HOST = "backup.example.com"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/path/to/the/db.sqlite3",
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "change me!"

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
