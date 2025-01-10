from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import user

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = user
        fields = ('email', 'username', 'first_name', 'last_name', 'phone_number', 'role')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = user
        fields = ('email', 'username', 'first_name', 'last_name', 'phone_number', 'role')
