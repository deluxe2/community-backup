# Community Backup

A website to manage backup repositories.

## Installation

This installation guide assumes a Debian 13 system.

Install Python and several dependencies:

This example should wo

```bash
apt update && apt install python3 python3-pip python3-venv borgbackup
```

Clone the repository

git clone https://git.srvspace.net/jo/community-backup.git

Or install from a release

Create a venv

```bash
python3 -m venv venv
```

Activea the venv

```bash
source venv/bin/activate
```

Install the package and it's dependencies:

```bash
pip install -e community-backup
```

Create a configuration file in `community_backup/community_backup/community_backup/configration.py`, e.g. by copying and adjusting the `example_configuraton.py` next to that location.

The settings are explained in detail in the setting section.

Apply the migrations:

```bash
python community-backup/community_backup/manage.py migrate
```

Collect the static files:

```bash
# python community-backup/community_backup/manage.py collectstatic

130 static files copied to '/opt/community_backup/static'.
```

Point your webserver to the static files. E.g. with caddy:

```
example.backups.org {
	handle /static/* {
		file_server {
			root /opt/community_backup/
		}
	}

	handle {
		reverse_proxy http://localhost:8000
	}
}
```

Create a superuser account

```

```

## Custom pages

Some pages are specific to your installation. E.g. an imprint.

Those files are markdown files that are rendered as HTML. You have to supply them and put them into the `MARKDOWN_PAGE_DIR`.

The following files are expected:

* `imprint.md` with your imprint information.

## Settings

### BACKUP_USER

`BACKUP_USER` specifies the username, that is used for borg backups. This user is used for various file permissions as well as the user that clients are using to log in and push their backups.

### BACKUP_REPO_HOST

`BACKUP_REPO_HOST` is the hostname given to the user for pushing their backups to. E.g. `backup.example.com`.

### BACKUP_HOME_DIR

`BACKUP_HOME_DIR` is the home directory of the borg user. This must be a `pathlib.Path`.

### BACKUP_BORG_DIR

`BACKUP_BORG_DIR` is the directory in which the actual backups are stored. This must be a `pathlib.Path`

### BACKUP_AUTHORIZED_KEYS

`BACKUP_AUTHORIZED_KEYS` is the authorized_keys file of the SSH daemon used for `BORG_USER`. This must be a `pathlib.Path`

### DATABASES

`DATABASES` is the Django database setting. Here is an example for sqlite3.

```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/some/path/to/db.sqlite3",
    }
}
```

### SECRET_KEY

The secret key used by django for session cookies and other things.

### DEBUG

Django debug setting.

### MARKDOWN_PAGE_DIR

`MARKDOWN_PAGE_DIR` is the directory where customized markdown files are put. This directory is required.

### BACKUP_MANAGE_PY

`BACKUP_MANAGE_PY` is the command to run the `manage.py` file, including e.g. a Python interpreter, venv, etc. This must be a `pathlib.Path`

### ADDITIONAL_FOOTER_NAV_ITEMS

`ADDITIONAL_FOOTER_NAV_ITEMS` allows you to add additional links to the footer. This is a `list[str]`. Each item gets rendered as is into a `<li class=nav-item>`. So usually you want to continue the proper Bootstrap styling in the lst. E.g.:

```python
ADDITIONAL_FOOTER_NAV_ITEMS = ["""<a class="nav-link" href="https://example.com/>Example Link</a>""",]
```
