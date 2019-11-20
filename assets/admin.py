import xlwt
from django.contrib import admin
from django.contrib.postgres import fields
from django.http import HttpResponse

from assets.forms import AssetForm
from assets.models import (AssetItem, Asset, AssetType, SupportReport, SupportTicket, SupportTicketItem,
                           AssetItemSupplyOrder)

from django_json_widget.widgets import JSONEditorWidget
from rangefilter.filter import DateRangeFilter

admin.site.register(AssetType, admin.ModelAdmin)
admin.site.register(AssetItemSupplyOrder, admin.ModelAdmin)


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


def export_excel(modeladmin, request, queryset):
    columns = ('UUID', 'Тип актива', 'Название актива', 'Дата получения',
               'Рекомендованное время использования, лет', 'Закупочная себестоимость', 'Амортизации использовано',
               'Амортизации осталось', 'Колличество обслуживающих работ', 'Дата последних обслуживающих работ',
               'Ожидаемая дата списания')

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="assets.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    for name in set(queryset.values_list('asset__name', flat=True).distinct()):
        q_list = list(queryset.filter(asset__name=name))
        objects = ((
            i.uuid,
            i.asset.asset_type.name,
            i.asset.name,
            i.date_acquire.strftime("%d.%m.%y"),
            i.years_to_use,
            i.sum_acquire,
            i.amortization_used,
            i.amortization_left,
            i.support_count,
            i.last_support,
            i.date_expire.strftime("%d.%m.%y")
        ) for i in q_list)

        ws = wb.add_sheet(name)
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        for row in objects:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)
    return response


@admin.register(AssetItem)
class AssetItemAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'asset', 'date_acquire', 'sum_acquire', 'years_to_use', 'date_expire',
                    'amortization_used', 'amortization_left', 'support_count', 'last_support')
    search_fields = ('asset__name',)
    list_filter = ('asset__asset_type', ('date_acquire', DateRangeFilter),)
    actions = (export_excel,)


class SupportTicketItemInline(admin.StackedInline):
    model = SupportTicketItem
    can_delete = True
    verbose_name_plural = 'Ордеры на материалы'


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'asset_item', 'time_planned', 'support_ticket_count')
    search_fields = ('asset_item__asset__name',)
    list_filter = ('asset_item__asset__asset_type', 'asset_item__asset__name', ('time_planned', DateRangeFilter),
                   ('time_created', DateRangeFilter))
    inlines = (SupportTicketItemInline,)


@admin.register(SupportReport)
class SupportReportAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'creator', 'time_created')
    search_fields = ('creator__email',)
    list_filter = (('time_created', DateRangeFilter),)
