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

MARKDOWN_PAGE_DIR = Path("./custom_md/")
BACKUP_MANAGE_PY = Path("/path/to/venv/bin/python /path/to/community_backup/manage.py")

# BORG_SERVER_PUBKEYS = [
#     (
#         "ecdsa-sha2-nistp256 AAAAASDJIASKJDASD root@example.com",
#         "256 SHA256:sTbOK9NvP1uUEixgUT8KUiYrY8J/DbK+jR39lwcT8Zw root@example.com (ECDSA)",
#     ),
#     (
#         "ssh-ed25519 AAAAasdiwdkjasdijwklajsdijasd root@example.com",
#         "256 SHA256:hPbWwRxNr1mFHZKYjcysnay1cQGQsOmDBvkA3Pzo4YY root@example.com (ED25519)",
#     ),
#     (
#         "ssh-rsa AAAABasdlkjasdiualksjd root@example.com",
#         "3072 SHA256:deuPTR8Hcc1LP7DHqAp91EINdLBQoco2IeMldIahamQ root@example.com (RSA)",
#     ),
# ]
