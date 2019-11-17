from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main.models import User
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


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
