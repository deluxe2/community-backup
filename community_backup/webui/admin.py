from django.contrib import admin
from django.urls import path, reverse_lazy
from django.views.generic import FormView
from django import forms

from .models import BorgRepository, Voucher


class VoucherBulkCreateForm(forms.Form):
    prefix = forms.CharField(label="Voucher prefix")
    amount = forms.IntegerField(label="Amount")


class VoucherBulkCreateView(FormView):
    form_class = VoucherBulkCreateForm
    template_name = "admin/bulk_generate.html"
    admin_site_context = None
    success_url = reverse_lazy("admin:webui_voucher_changelist")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # inject the admin site context so that the navbar and other things work as intended
        context.update(self.admin_site_context.each_context(self.request))
        return context

    def form_valid(self, form):
        Voucher.bulk_generate(form.cleaned_data["prefix"], form.cleaned_data["amount"])
        return super().form_valid(form)


@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    change_list_template = "admin/voucher_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "bulk_generate/",
                self.admin_site.admin_view(
                    VoucherBulkCreateView.as_view(admin_site_context=self.admin_site)
                ),
                name="voucher_bulk_generate",
            )
        ]
        return my_urls + urls


# Register your models here.
admin.site.register(BorgRepository)
