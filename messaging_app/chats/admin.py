from django.contrib import admin
from .models import user, Message, Conversation

# Register your models here.


class UserAdminConfig(admin.ModelAdmin):
    ordering = ('created_at',)
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff')

admin.site.register(user, UserAdminConfig)
admin.site.register(Message)
admin.site.register(Conversation)