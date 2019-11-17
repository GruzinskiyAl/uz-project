from django.contrib.auth.forms import UserChangeForm
from main.models import User


class CustomChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'role',
                  'phone',
                  'email',
                  'manager',
                  'user_status')
