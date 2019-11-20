import xlwt
from django.contrib import admin
from django.http import HttpResponse

from material.models import Material, MaterialCategory, SupplyOrder, UsageOrder
from django_json_widget.widgets import JSONEditorWidget
from rangefilter.filter import DateRangeFilter
from django.contrib.postgres import fields

admin.site.register(MaterialCategory, admin.ModelAdmin)


def export_excel(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="materials.xls"'
    wb = xlwt.Workbook(encoding='utf-8')

    for name in set(queryset.values_list('category__name', flat=True).distinct()):
        columns = ['UUID', 'Категория', 'Наименование', "Закупочная себестоимость", "Доступное колличество",
                   "Общая себестоимость", "Последняя дата закупки"]
        filtered_queryset = queryset.filter(category__name=name)
        q_list = list(filtered_queryset)

        extra_columns = []
        for obj in filtered_queryset:
            for i in obj.info.keys():
                extra_columns.append(i)
        extra_columns = list(set(extra_columns))

        objects = []
        for obj in q_list:
            obj_data = [str(obj.uuid), obj.category.name, obj.name, obj.price,
                        obj.count, obj.sum_price, obj.last_supply_date]
            for key in extra_columns:
                obj_data.append(obj.info.get(key, ''))
            objects.append(obj_data)

        ws = wb.add_sheet(name)
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        for col_num in range(len(columns+extra_columns)):
            ws.write(row_num, col_num, (columns+extra_columns)[col_num], font_style)
        font_style = xlwt.XFStyle()
        for row in objects:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)
    return response


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    formfield_overrides = (
        {
            fields.JSONField: {'widget': JSONEditorWidget},
        }
    )
    list_display = ('uuid', 'name', 'category', 'price', 'count', 'sum_price')
    list_filter = ('category__name',)
    search_fields = ('name', 'uuid')
    actions = (export_excel, )


@admin.register(SupplyOrder)
class SupplyOrderAdmin(admin.ModelAdmin):
    list_display = ('material', 'responsive_user', 'date', 'count_in')
    list_filter = ('material__category', ('date', DateRangeFilter))


@admin.register(UsageOrder)
class SupplyOrderAdmin(admin.ModelAdmin):
    list_display = ('material', 'date', 'count_out')
    list_filter = ('material__category', ('date', DateRangeFilter))
