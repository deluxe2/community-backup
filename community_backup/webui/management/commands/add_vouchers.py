from django.core.management.base import BaseCommand
from random import choices
from ...models import Voucher


class Command(BaseCommand):
    help = "bulk-add vouchers with a given prefix and generate a latex output to render them"

    def add_arguments(self, parser):
        parser.add_argument("prefix", type=str)
        parser.add_argument("amount", type=int)

    def handle(self, *args, **options):
        vouchers = Voucher.bulk_generate(options["prefix"], options["amount"])

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
