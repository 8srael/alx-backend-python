from django.contrib import admin
from .models import Message, MessageHistory

admin.site.register(Message)
admin.site.register(MessageHistory)