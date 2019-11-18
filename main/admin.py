from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main.models import User, Role
from main.forms import CustomChangeForm
from django.contrib.auth.models import Group


class CustomUserAdmin(UserAdmin):
    form = CustomChangeForm
    model = User
    list_display = ('first_name',
                    'last_name',
                    'role',
                    'phone',
                    'email',
                    'manager',
                    'user_status')
    fieldsets = ()
    list_filter = ('role__name', 'user_status')
    search_fields = ('first_name', 'last_name', 'email')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Role, admin.ModelAdmin)
admin.site.unregister(Group)
