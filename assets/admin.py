from django.contrib import admin
from .models import *

admin.site.register(AssetType, admin.ModelAdmin)
admin.site.register(Asset, admin.ModelAdmin)
admin.site.register(AssetItem, admin.ModelAdmin)
admin.site.register(SupportTicket, admin.ModelAdmin)
admin.site.register(SupportTicketItem, admin.ModelAdmin)
admin.site.register(SupportReport, admin.ModelAdmin)
