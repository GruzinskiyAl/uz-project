from django.contrib import admin
from django.contrib.postgres import fields

from assets.forms import AssetForm
from assets.models import AssetItem, Asset, AssetType, SupportReport, SupportTicket, SupportTicketItem

from django_json_widget.widgets import JSONEditorWidget
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

admin.site.register(AssetType, admin.ModelAdmin)


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    form = AssetForm
    list_display = ('__str__', 'asset_type')
    list_filter = ('asset_type',)
    formfield_overrides = (
        {
            fields.JSONField: {'widget': JSONEditorWidget},
        }
    )


@admin.register(AssetItem)
class AssetItemAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'asset', 'date_acquire', 'sum_acquire', 'years_to_use', 'date_expire',
                    'amortization_used', 'amortization_left', 'support_count', 'last_support')
    search_fields = ('name',)
    list_filter = ('asset__asset_type', 'asset__name', ('date_acquire', DateRangeFilter),)


class SupportTicketItemInline(admin.StackedInline):
    model = SupportTicketItem
    can_delete = True
    verbose_name_plural = 'Ордеры на материалы'


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'asset_item', 'time_planned', 'support_ticket_count')
    search_fields = ('asset_item__name',)
    list_filter = ('asset_item__asset__asset_type', 'asset_item__asset__name', ('time_planned', DateRangeFilter),
                   ('time_created', DateRangeFilter))
    inlines = (SupportTicketItemInline,)


@admin.register(SupportReport)
class SupportReportAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'creator', 'time_created')
    search_fields = ('creator__email', )
    list_filter = (('time_created', DateRangeFilter),)
