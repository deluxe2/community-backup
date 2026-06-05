from django.core.management.base import BaseCommand
from random import choices
from ...models import Voucher


class Command(BaseCommand):
    help = "bulk-add vouchers with a given prefix and generate a latex output to render them"

    def add_arguments(self, parser):
        parser.add_argument("prefix", type=str)
        parser.add_argument("amount", type=int)

    def handle(self, *args, **options):
        unabmigous_characters = "abcdefghijkmnopqrstuvwxyzACDEFHJKLMNPQRTUVWXY1234679"

        vouchers = set()
        while len(vouchers) < options["amount"]:
            random_part = "".join(choices(unabmigous_characters, k=5))
            vouchers.add(f"{options['prefix']}-{random_part}")

        Voucher.objects.bulk_create(Voucher(code=v) for v in vouchers)

        header = r"""\begin{document}
\begin{center}
"""
        output = header
        even = False
        for v in vouchers:
            output += f"\\voucher{{{v}}}"
            if even:
                output += "\\newline\n"
            else:
                output += "\n"
            even = not even

        output += r"""\end{center}
\end{document}"""

        print(output)
