from random import choices
from pathlib import Path

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.conf import settings
import msgpack

from .tasks import update_user


# Create your models here.
class BorgRepository(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                r"[a-zA-Z0-9\-_]+", message="Only a-z, A-Z, 0-9, - and _ are allowed."
            )
        ],
    )
    key = models.TextField(
        validators=[
            RegexValidator(
                r"^(ssh\-rsa|ecdsa\-sha2\-nistp256|ssh\-ed25519) ([a-zA-Z0-9\+/=]+)( ([\S ]*))?$",
                message="not a valid SSH public key.",
            ),
        ]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    quota = models.IntegerField(default=500)
    used_quota = models.IntegerField(default=-1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("name", "user"), name="BorgRepository_name_user_unique"
            )
        ]

    def __str__(self):
        return f"BorgRepository '{self.user.username}' - '{self.name}' ({self.pk})"

    @property
    def path(self) -> Path:
        return settings.BACKUP_BORG_DIR / str(self.user.pk) / str(self.pk)

    @property
    def repo_url(self) -> str:
        return f"ssh://{settings.BACKUP_USER}@{settings.BACKUP_REPO_HOST}/./{self.user.pk}/{self.pk}"

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)
        update_user.enqueue()

    def delete(self):

        super().delete()
        update_user.enqueue()

    @property
    def key_type(self) -> str:
        return self.key.split(" ", 1)[0].strip()

    @property
    def key_value(self) -> str:
        return self.key.split(" ", 2)[1].strip()

    @property
    def key_comment(self) -> str | None:
        splits = self.key.split(" ", 2)
        if len(splits) == 3:
            return splits[2].strip()
        return None

    def truncated_key(self, length: int = 60):
        """
        Returns a truncated version of the key for display purposes.
        The Key type and the comment are retained as much as possible.
        """

        # check how long the truncated part of the key may be at most.
        max_len = length - len(self.key_type) - 1
        if self.key_comment:
            max_len = max_len - len(self.key_comment) - 1

        if len(self.key_value) > max_len:
            max_len -= 1  # remove one character if we add an ellipsis
            trunc_key = self.key_value[:max_len] + "…"
        else:
            trunc_key = self.key_value

        output = f"{self.key_type} {trunc_key}"

        if self.key_comment:
            output += f" {self.key_comment}"

        return output

    def refresh_quota(self):
        hints_files = self.path.glob("hints.*")

        try:
            hint = next(hints_files)
            data = hint.open(mode="rb").read()

            unpacked = msgpack.unpackb(data, strict_map_key=False, raw=True)
            quota_used = unpacked[b"storage_quota_use"]

            self.used_quota = int(quota_used / 10**9)
        except StopIteration:
            # No hints file found, therefore the repo is probably not initialized
            self.used_quota = -1


class Voucher(models.Model):
    used = models.BooleanField(default=False)
    code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Voucher '{self.code}'"

    @classmethod
    def bulk_generate(cls, prefix: str, amount: int) -> set[str]:
        """
        Create `amount` vouchers starting with `prefix`.

        Returns a set of the voucher codes as strings.
        """
        unabmigous_characters = "abcdefghijkmnopqrstuvwxyzACDEFHJKLMNPQRTUVWXY1234679"

        vouchers = set()
        while len(vouchers) < amount:
            random_part = "".join(choices(unabmigous_characters, k=5))
            vouchers.add(f"{prefix}-{random_part}")

        Voucher.objects.bulk_create(Voucher(code=v) for v in vouchers)
        return vouchers
