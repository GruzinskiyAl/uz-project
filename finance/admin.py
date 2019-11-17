from django.contrib import admin
from .models import *


@admin.register(Cash)
class CashAdmin(admin.ModelAdmin):
    def add_view(self, request, form_url='', extra_context=None):
        pass


admin.site.register(CreditTicket, admin.ModelAdmin)
admin.site.register(ChargeTicket, admin.ModelAdmin)
