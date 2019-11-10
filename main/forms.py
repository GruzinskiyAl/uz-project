from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from main.models import User


class CustomCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('phone', 'position')


class CustomChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('phone', 'position')
