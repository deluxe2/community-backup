from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from webui.models import BorgRepository


class BorgRepositoryTestCase(TestCase):
    def test_ssh_key_regex(self):
        user = User.objects.create(username="foo")

        # good repo
        repo = BorgRepository.objects.create(
            name="test1",
            key="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOYOkeGl40Bss9LMmreCtzq+uXw4IQ/E5SKsBRcKAfF3 jo@hubris",
            user=user,
        )

        repo.full_clean()

        # good repo, key without comment
        repo = BorgRepository.objects.create(
            name="test2",
            key="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOYOkeGl40Bss9LMmreCtzq+uXw4IQ/E5SKsBRcKAfF3",
            user=user,
        )
        repo.full_clean()

        # bad repo (wrong key)
        repo = BorgRepository.objects.create(name="test3", key="Foo", user=user)
        self.assertRaises(ValidationError, repo.full_clean)

        # bad repo (multiple valid keys )
        repo = BorgRepository.objects.create(
            name="test4",
            key="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOYOkeGl40Bss9LMmreCtzq+uXw4IQ/E5SKsBRcKAfF3 jo@hubris\nssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOYOkeGl40Bss9LMmreCtzq+uXw4IQ/E5SKsBRcKAfF3 jo@hubris",
            user=user,
        )
        self.assertRaises(ValidationError, repo.full_clean)

        # bad repo, leading whitespace
        repo = BorgRepository.objects.create(
            name="test5",
            key=" ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOYOkeGl40Bss9LMmreCtzq+uXw4IQ/E5SKsBRcKAfF3 jo@hubris",
            user=user,
        )
        self.assertRaises(ValidationError, repo.full_clean)

        # good repo, with whitespace in commment
        repo = BorgRepository.objects.create(
            name="test6",
            key="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOYOkeGl40Bss9LMmreCtzq+uXw4IQ/E5SKsBRcKAfF3 jo@hubris whitespace in comment",
            user=user,
        )
        repo.full_clean()
