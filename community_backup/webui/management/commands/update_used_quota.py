from django.core.management.base import BaseCommand
from ...models import BorgRepository


class Command(BaseCommand):
    help = "Update the used quota values"

    def add_arguments(self, parser):
        parser.add_argument("--user-id", type=int)
        parser.add_argument("--repository-id", type=int, nargs="+")

    def handle(self, *args, **options):
        qs = BorgRepository.objects.all()

        if options.get("user_id"):
            qs = qs.filter(user__pk=options.get("user_id"))

        if options.get("repository_id"):
            qs = qs.filter(pk__in=options.get("repository_id"))

        for repo in qs:
            repo.refresh_quota()

        BorgRepository.objects.bulk_update(qs, ["used_quota"])
