from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.conf import settings
from pathlib import Path


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
                r"(ssh\-rsa|ecdsa\-sha2\-nistp256|ssh\-ed25519) ([a-zA-Z0-9\+/=]+) (\S*)",
                message="not a valid SSH public key.",
            ),
        ]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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
        return f"{settings.BACKUP_USER}@{settings.BACKUP_REPO_HOST}:{self.user.pk}/{self.pk}"

    def save(self):

        super().save()
        update_user.enqueue()

    def delete(self):

        super().delete()
        update_user.enqueue()


class Voucher(models.Model):
    used = models.BooleanField(default=False)
    code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Voucher '{self.code}'"
