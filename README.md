# ![Logo](community_backup/static/webui/logo.png) Community Backup

A website to manage backup repositories.

> **Note:** This is a fork of [Community Backup](https://git.srvspace.net/jo/community-backup) by jo,
> licensed under the [GNU Affero General Public License v3.0](LICENSE). This fork is distributed
> under the same license. Changes from the original are recorded in the git history of this repository.

## Installation

This installation guide assumes a Debian 13 system.

Install Python and several dependencies:

This example should wo

```bash
apt update && apt install python3 python3-pip python3-venv borgbackup
```

Clone the repository

git clone https://github.com/deluxe2/community-backup.git

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

### Repository Quota Updates

The repository quotas in the UI are updated after each backup.
To update the quota during an operation the `update_used_quota` management command can be executed on a regular basis.

There are example configs for systemd-timers in `contrib/communitybackup-quota-update.service` and `contrib/communitybackup-quota-update.timer`. Adjust the paths and the timers to your needs.


## Custom pages

Some pages are specific to your installation. E.g. an imprint.

Those files are markdown files that are rendered as HTML. You have to supply them and put them into the `MARKDOWN_PAGE_DIR`.

The following files are expected:

* `imprint.md` with your imprint information.
* `privacy_policy.md` with your privacy policy.

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

### BORG_SERVER_PUBKEYS

A list of the SSH public keys and their hashes to verify the server a User is connecting to.
This is a list of tuples, containing the key and it's hash.

```python
BORG_SERVER_PUBKEYS = [
    (
        "ecdsa-sha2-nistp256 AAAAASDJIASKJDASD root@example.com",
        "256 SHA256:sTbOK9NvP1uUEixgUT8KUiYrY8J/DbK+jR39lwcT8Zw root@example.com (ECDSA)",
    ),
    (
        "ssh-ed25519 AAAAasdiwdkjasdijwklajsdijasd root@example.com",
        "256 SHA256:hPbWwRxNr1mFHZKYjcysnay1cQGQsOmDBvkA3Pzo4YY root@example.com (ED25519)",
    ),
    (
        "ssh-rsa AAAABasdlkjasdiualksjd root@example.com",
        "3072 SHA256:deuPTR8Hcc1LP7DHqAp91EINdLBQoco2IeMldIahamQ root@example.com (RSA)",
    ),
]
```

## Webserver Config / Content-Security-Policy

This page by itself does not load external sources and does not use inline javascript/styling.
It only loads javascript, CSS and images.
Therefore the following Content-Security-Policy should work fine in the standard cases:

```
Content-Security-Policy "default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self';"
```
