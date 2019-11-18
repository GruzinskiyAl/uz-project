from datetime import date

from django.contrib import admin
from finance.models import Cash, Ticket


@admin.register(Cash)
class CashAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        if Cash.objects.filter(date=date.today()).exists():
            return False
        return super().has_add_permission(request)


admin.site.register(Ticket, admin.ModelAdmin)
