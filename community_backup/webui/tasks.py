from django.tasks import task
from .deployments import sync_repos


@task
def update_user():
    sync_repos()
