from django.contrib import admin
from .models import *

admin.site.register(MaterialCategory, admin.ModelAdmin)
admin.site.register(Material, admin.ModelAdmin)
admin.site.register(SupplyOrder, admin.ModelAdmin)
admin.site.register(UsageOrder, admin.ModelAdmin)
