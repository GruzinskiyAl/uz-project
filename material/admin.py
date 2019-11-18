from django.contrib import admin
from material.models import Material, MaterialCategory, SupplyOrder, UsageOrder
from django_json_widget.widgets import JSONEditorWidget
from rangefilter.filter import DateRangeFilter
from django.contrib.postgres import fields
admin.site.register(MaterialCategory, admin.ModelAdmin)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    formfield_overrides = (
        {
            fields.JSONField: {'widget': JSONEditorWidget},
        }
    )
    list_display = ('uuid', 'name', 'category', 'price', 'count', 'sum_price')
    list_filter = ('category__name', )
    search_fields = ('name', 'uuid')


@admin.register(SupplyOrder)
class SupplyOrderAdmin(admin.ModelAdmin):
    list_display = ('material', 'responsive_user', 'date', 'count_in')
    list_filter = ('material__category', ('date', DateRangeFilter))


@admin.register(UsageOrder)
class SupplyOrderAdmin(admin.ModelAdmin):
    list_display = ('material', 'responsive_user', 'date', 'count_out')
    list_filter = ('material__category', ('date', DateRangeFilter))
