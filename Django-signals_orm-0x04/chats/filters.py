"""
    This file contains the filter class for the Message model.
    The filter class is used to filter the messages based on the sender, recipient, and date range.
"""


import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.CharFilter(field_name='sender__username', lookup_expr='icontains')
    recipient = django_filters.CharFilter(field_name='recipient__username', lookup_expr='icontains')
    date_range = django_filters.DateFromToRangeFilter(field_name='created_at')

    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'date_range']
