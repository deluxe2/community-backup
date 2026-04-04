from pathlib import Path
from subprocess import run
from collections import defaultdict
from typing import Any
from logging import getLogger
import shutil

from django.contrib.auth.models import User

from .models import BorgRepository

logger = getLogger("deployments")

# sync users


def get_users(user_prefix: str = "u-") -> dict[str, dict[str, Any]]:

    passwd = Path("/etc/passwd").read_text()
    output = dict()
    for line in passwd.splitlines():
        name, _, _, _, _, homedir, _ = line.split(":")
        if not name.startswith(user_prefix):
            continue

        output[name] = {"homedir": Path(homedir)}

    return output


def cleanup_users(
    usernames: set[str],
    system_users: dict[str, dict[str, Any]],
    dry_run=False,
):
    """Cleans up all unused user accounts and directories on the system.

    usernames is the set of users that should exist.
    system_users contains all the users that exist (with the correct prefix)"""

    base_dir = Path("/home/")

    # cleanup users
    for user in system_users.keys():
        if user not in usernames:
            logger.info("Deleting user '%(user)s'.")
            print(f"Deleting user '{user}'.")
            if not dry_run:
                run(["userdel", user])
                pass

    # cleanup directories
    for dir in base_dir.iterdir():
        if dir.is_dir() and dir.name.startswith("u-") and dir.name not in usernames:
            logger.info("Deleting home directory '%(dir)s'")
            print(f"Deleting home directory '{dir}'")
            if not dry_run:
                shutil.rmtree(dir)
                pass


def create_users(
    usernames: set[str],
    system_users: dict[str, dict[str, Any]],
    dry_run=False,
):

    for username in usernames:
        if username not in system_users.keys():
            logger.info("Adding user '%(username)s'")
            print(f"Adding user '{username}'")
            if not dry_run:
                add_user(username)


def add_user(username: str):

    users = get_users()
    assert username not in users.keys(), "User already exists"

    run(["useradd", "--no-user-group", "--create-home", username], check=True)


def sync_users(dry_run=False):

    # gather data
    users = User.objects.all()
    usernames = {f"u-{user.pk}" for user in users}
    system_users = get_users()

    # clean up old users
    cleanup_users(usernames=usernames, system_users=system_users, dry_run=dry_run)

    # create the new users
    create_users(usernames=usernames, system_users=system_users, dry_run=dry_run)

    for user in users:
        username = f"u-{user.pk}"
        sync_repos(
            username=username,
            user=user,
            system_user=system_users[username],
            dry_run=dry_run,
        )


# sync authorized_keys
def sync_repos(username: str, user: User, system_user: dict[str, Any], dry_run=False):

    repos = BorgRepository.objects.filter(user=user)

    repos_by_key = defaultdict(list)
    for repo in repos:
        repos_by_key[repo.key].append(repo)

    homedir = system_user["homedir"]

    # create .ssh directory
    ssh_dir = homedir / ".ssh"
    ssh_dir.mkdir(
        mode=0o750,
        exist_ok=True,
        parents=True,
    )

    # create authorized_keys file
    authorized_keys = ssh_dir / "authorized_keys"

    commands = []
    for key, repos in repos_by_key.items():
        repo_paths = [
            f"--restrict-to-repository {str(system_user['homedir'] / repo.name)}"
            for repo in repos
        ]
        commands.append(
            f"""command="borg serve {" ".join(repo_paths)} --quota=500G",restrict ssh-rsa {key}"""
        )

    print("\n".join(commands))

    authorized_keys.write_text("\n".join(commands) + "\n")

    # remove repositories that do no longer exist
    repo_names = {repo.name for repo in repos}
    print(repo_names)
    for dir in homedir.iterdir():
        print(dir.name)
        if dir.is_dir() and not dir.name.startswith("."):
            if dir.name not in repo_names:
                print(f"removing unused repo '{dir}'")
                shutil.rmtree(dir)

    # create the repositories
    for repo in repos:
        path = system_user["homedir"] / repo.name
        path.mkdir(mode=0o750, exist_ok=True, parents=True)
        shutil.chown(path, user=username)
