from django.core.management.base import BaseCommand
from ...deployments import sync_repos


class Command(BaseCommand):
    help = "Synchronized users on the host with the database."

    def handle(self, *args, **options):
        sync_repos(dry_run=False)
