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
    list_display = ('__str__', 'asset_type', 'years_to_use', 'supply_orders_count')
    list_filter = ('asset_type__name',)
    formfield_overrides = (
        {
            fields.JSONField: {'widget': JSONEditorWidget},
        }
    )

    def supply_orders_count(self, obj):
        return obj.supply_orders_count

    supply_orders_count.short_description = 'Количество закупок'


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

    def years_to_use(self, obj):
        return obj.years_to_use

    def amortization_used(self, obj):
        return obj.amortization_used

    def amortization_left(self, obj):
        return obj.amortization_left

    def support_count(self, obj):
        return obj.support_count

    def last_support(self, obj):
        return obj.last_support

    def date_expire(self, obj):
        return obj.date_expire

    years_to_use.short_description = "Время эксплуатации (лет)"
    amortization_used.short_description = "Амортизации использовано"
    amortization_left.short_description = "Амортизации осталось"
    support_count.short_description = "Количество ремонтных работ"
    last_support.short_description = "Дата последних работ"
    date_expire.short_description = "Дата списания"

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class SupportTicketItemInline(admin.StackedInline):
    model = SupportTicketItem
    can_delete = True
    verbose_name_plural = 'Ордеры на материалы'


def export_support_excel(modeladmin, request, queryset):
    columns = ("Запланированная дата", "Еденица актива", "Количество выдачей на материалы", "Описание")

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="supports.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    objects = ((
        i.time_planned.strftime("%d.%m.%y"),
        i.asset_item.__str__(),
        i.support_ticket_count,
        i.description
    ) for i in queryset)

    ws = wb.add_sheet("Ремонтные работы")
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


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'asset_item', 'time_planned', 'support_ticket_count')
    search_fields = ('asset_item__asset__name',)
    list_filter = ('asset_item__asset__asset_type', 'asset_item__asset__name', ('time_planned', DateRangeFilter),
                   ('time_created', DateRangeFilter))
    inlines = (SupportTicketItemInline,)

    actions = (export_support_excel, )

    def support_ticket_count(self, obj):
        return obj.support_ticket_count

    support_ticket_count.short_description = 'Количество выдачей на материалы'


def export_reports_excel(modeladmin, request, queryset):
    columns = ("Запланированная дата", "Еденица актива", "Ответственный",
               "Дата отчета", "Описание")

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="supports.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    objects = ((
        i.support_ticket.time_planned.strftime("%d.%m.%y"),
        i.support_ticket.asset_item.__str__(),
        i.creator.full_name,
        i.time_created.strftime("%d.%m.%y"),
        i.description
    ) for i in queryset)

    ws = wb.add_sheet("Ремонтные работы")
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

@admin.register(SupportReport)
class SupportReportAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'creator', 'time_created')
    search_fields = ('creator__email',)
    list_filter = (('time_created', DateRangeFilter),)
    actions = (export_reports_excel, )