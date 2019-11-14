from django.contrib import admin
from .models import *

admin.site.register(Cash, admin.ModelAdmin)
admin.site.register(CreditTicket, admin.ModelAdmin)
admin.site.register(ChargeTicket, admin.ModelAdmin)
