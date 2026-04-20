from collections import defaultdict
from logging import getLogger
import shutil


from django.conf import settings


logger = getLogger("deployments")


def sync_repos(dry_run=False):
    """Synchronize the repos"""
    from .models import BorgRepository

    repos = BorgRepository.objects.all()

    repos_by_key = defaultdict(list)
    for repo in repos:
        repos_by_key[f"{repo.key_type} {repo.key_value}"].append(repo)

    # create .ssh directory
    ssh_dir = settings.BACKUP_AUTHORIZED_KEYS.parent
    if not dry_run:
        ssh_dir.mkdir(
            mode=0o750,
            exist_ok=True,
            parents=True,
        )

    # create authorized_keys file
    authorized_keys = settings.BACKUP_AUTHORIZED_KEYS

    commands = []
    for key, repositories in repos_by_key.items():
        repo_paths = [f"--restrict-to-repository {repo.path}" for repo in repositories]
        quota = max(repo.quota for repo in repositories)
        ids = [str(repo.id) for repo in repositories]
        commands.append(
            f"""command="cd {str(settings.BACKUP_BORG_DIR)}; borg serve {" ".join(repo_paths)} --storage-quota={quota}G;{settings.BACKUP_MANAGE_PY} update_used_quota --repository-id {" ".join(ids)}",restrict {key}"""
        )

    if not dry_run:
        authorized_keys.write_text("\n".join(commands) + "\n")

    # remove repositories that do no longer exist
    repo_paths = {repo.path for repo in repos}
    for user_dir in settings.BACKUP_BORG_DIR.iterdir():
        print(user_dir)
        for dir in user_dir.iterdir():
            if dir.is_dir() and not dir.name.startswith("."):
                if dir not in repo_paths:
                    print(f"removing unused repo '{dir}'")
                    if not dry_run:
                        shutil.rmtree(dir)

    # create the repositories
    for repo in repos:
        print(f"creating repo {repo}")
        if not dry_run:
            repo.path.mkdir(mode=0o750, exist_ok=True, parents=True)
            shutil.chown(repo.path, user=settings.BACKUP_USER)
