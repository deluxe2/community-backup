from .models import BorgRepository
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Voucher


class BorgRepositoryForm(forms.ModelForm):
    class Meta:
        fields = ["name", "key", "user"]
        model = BorgRepository
        widgets = {"user": forms.HiddenInput()}


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    voucher = forms.CharField(help_text="Your registration voucher.")

    def clean_voucher(self):
        obj = Voucher.objects.filter(code=self.cleaned_data["voucher"], used=False)

        if not obj.exists():
            raise ValidationError(
                "Voucher code '%(code)s' is invalid",
                code="invalid",
                params={"code": self.cleaned_data["voucher"]},
            )

        return obj.first()

    def save(self, commit=True):
        voucher = self.cleaned_data["voucher"]

        voucher.used = True
        voucher.save()
        super().save(commit)

    class Meta(UserCreationForm.Meta):
        fields = ("username", "email")
