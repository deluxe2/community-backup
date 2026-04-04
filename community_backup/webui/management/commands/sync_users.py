from django.core.management.base import BaseCommand, CommandError
from ...models import BorgRepository
from ...deployments import sync_users


class Command(BaseCommand):
    help = "Synchronized users on the host with the database."

    def handle(self, *args, **options):

        repos = BorgRepository.objects.all()

        for repo in repos:
            self.stdout.write(f"{repo}")
        self.stdout.write(self.style.SUCCESS("This is a test"))

        sync_users(dry_run=False)
