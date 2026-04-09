# enter your overrides here
from pathlib import Path

BACKUP_HOME_DIR = Path("/data/backups")
BACKUP_BORG_DIR = BACKUP_HOME_DIR / "borg"
BACKUP_AUTHORIZED_KEYS = BACKUP_HOME_DIR / ".ssh" / "authorized_keys"
BACKUP_USER = "borg"
BACKUP_REPO_HOST = "backup.example.com"
