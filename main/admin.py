from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from main.models import User
from main.forms import CustomChangeForm, CustomCreationForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomCreationForm
    form = CustomChangeForm
    model = User


admin.site.register(User, CustomUserAdmin)
# admin.site.register(BaseAsset, admin.ModelAdmin)
