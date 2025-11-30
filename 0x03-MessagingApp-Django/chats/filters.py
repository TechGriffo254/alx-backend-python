"""Filter classes for the messaging application."""
import django_filters
from django.db.models import Q
from .models import Message, Conversation


class MessageFilter(django_filters.FilterSet):
    """
    Filter class for Message model.
    
    Supports filtering by:
    - conversation_id: Filter messages by conversation
    - sender_id: Filter messages by sender
    - sent_after: Filter messages sent after a specific datetime
    - sent_before: Filter messages sent before a specific datetime
    - search: Search in message body
    """
    
    conversation_id = django_filters.UUIDFilter(
        field_name='conversation__conversation_id',
        lookup_expr='exact'
    )
    
    sender_id = django_filters.UUIDFilter(
        field_name='sender__user_id',
        lookup_expr='exact'
    )
    
    sent_after = django_filters.DateTimeFilter(
        field_name='sent_at',
        lookup_expr='gte',
        label='Sent after (YYYY-MM-DD HH:MM:SS)'
    )
    
    sent_before = django_filters.DateTimeFilter(
        field_name='sent_at',
        lookup_expr='lte',
        label='Sent before (YYYY-MM-DD HH:MM:SS)'
    )
    
    date_range = django_filters.DateFromToRangeFilter(
        field_name='sent_at',
        label='Date range'
    )
    
    search = django_filters.CharFilter(
        method='filter_search',
        label='Search in message body'
    )
    
    def filter_search(self, queryset, name, value):
        """
        Custom search filter for message body.
        """
        return queryset.filter(
            Q(message_body__icontains=value)
        )
    
    class Meta:
        model = Message
        fields = ['conversation_id', 'sender_id', 'sent_after', 'sent_before', 'search']


class ConversationFilter(django_filters.FilterSet):
    """
    Filter class for Conversation model.
    
    Supports filtering by:
    - participant_id: Filter conversations by participant
    - created_after: Filter conversations created after a specific datetime
    - created_before: Filter conversations created before a specific datetime
    """
    
    participant_id = django_filters.UUIDFilter(
        field_name='participants__user_id',
        lookup_expr='exact',
        label='Filter by participant ID'
    )
    
    participant_username = django_filters.CharFilter(
        field_name='participants__username',
        lookup_expr='icontains',
        label='Filter by participant username'
    )
    
    created_after = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Created after (YYYY-MM-DD HH:MM:SS)'
    )
    
    created_before = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte',
        label='Created before (YYYY-MM-DD HH:MM:SS)'
    )
    
    date_range = django_filters.DateFromToRangeFilter(
        field_name='created_at',
        label='Date range'
    )
    
    class Meta:
        model = Conversation
        fields = ['participant_id', 'participant_username', 'created_after', 'created_before']
