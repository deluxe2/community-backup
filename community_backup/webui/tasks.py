from django.tasks import task
from .deployments import sync_repos, get_users
from django.contrib.auth.models import User


@task
def update_user(user_pk):
    user = User.objects.get(pk=user_pk)
    username = f"u-{user.pk}"
    system_user = get_users()[username]

    sync_repos(username=username, user=user, system_user=system_user)
