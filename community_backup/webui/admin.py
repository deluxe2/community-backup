from django.contrib import admin

from .models import BorgRepository, Voucher

# Register your models here.
admin.site.register(BorgRepository)
admin.site.register(Voucher)
