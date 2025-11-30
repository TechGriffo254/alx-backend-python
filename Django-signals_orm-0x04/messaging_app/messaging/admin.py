"""
Admin configuration for the messaging app.

Registers all models with the Django admin interface with
enhanced functionality for managing messages, notifications,
and message history.
"""

from django.contrib import admin
from .models import Message, Notification, MessageHistory


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Admin interface for the Message model.
    
    Provides comprehensive view and filtering options for managing messages.
    """
    
    list_display = [
        'id',
        'sender',
        'receiver',
        'truncated_content',
        'timestamp',
        'edited',
        'read',
        'parent_message',
    ]
    
    list_filter = [
        'edited',
        'read',
        'timestamp',
    ]
    
    search_fields = [
        'sender__username',
        'receiver__username',
        'content',
    ]
    
    readonly_fields = [
        'timestamp',
        'edited',
    ]
    
    raw_id_fields = [
        'sender',
        'receiver',
        'parent_message',
    ]
    
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('Message Info', {
            'fields': ('sender', 'receiver', 'content')
        }),
        ('Threading', {
            'fields': ('parent_message',),
            'description': 'Set parent message for threaded conversations'
        }),
        ('Status', {
            'fields': ('read', 'edited', 'timestamp'),
        }),
    )
    
    def truncated_content(self, obj):
        """Display truncated message content in the list view."""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    
    truncated_content.short_description = 'Content'
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        qs = super().get_queryset(request)
        return qs.select_related('sender', 'receiver', 'parent_message')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin interface for the Notification model.
    
    Allows viewing and managing user notifications.
    """
    
    list_display = [
        'id',
        'user',
        'notification_type',
        'truncated_content',
        'timestamp',
        'read',
        'message',
    ]
    
    list_filter = [
        'notification_type',
        'read',
        'timestamp',
    ]
    
    search_fields = [
        'user__username',
        'content',
        'notification_type',
    ]
    
    readonly_fields = [
        'timestamp',
    ]
    
    raw_id_fields = [
        'user',
        'message',
    ]
    
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('Notification Info', {
            'fields': ('user', 'message', 'notification_type', 'content')
        }),
        ('Status', {
            'fields': ('read', 'timestamp'),
        }),
    )
    
    def truncated_content(self, obj):
        """Display truncated notification content in the list view."""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    
    truncated_content.short_description = 'Content'
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        qs = super().get_queryset(request)
        return qs.select_related('user', 'message')


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    """
    Admin interface for the MessageHistory model.
    
    Displays the edit history of messages.
    """
    
    list_display = [
        'id',
        'message',
        'truncated_old_content',
        'edited_at',
        'edited_by',
    ]
    
    list_filter = [
        'edited_at',
    ]
    
    search_fields = [
        'old_content',
        'message__content',
        'edited_by__username',
    ]
    
    readonly_fields = [
        'message',
        'old_content',
        'edited_at',
        'edited_by',
    ]
    
    raw_id_fields = [
        'message',
        'edited_by',
    ]
    
    date_hierarchy = 'edited_at'
    
    fieldsets = (
        ('History Info', {
            'fields': ('message', 'old_content', 'edited_by', 'edited_at')
        }),
    )
    
    def truncated_old_content(self, obj):
        """Display truncated old content in the list view."""
        return obj.old_content[:50] + '...' if len(obj.old_content) > 50 else obj.old_content
    
    truncated_old_content.short_description = 'Old Content'
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        qs = super().get_queryset(request)
        return qs.select_related('message', 'edited_by')
    
    def has_add_permission(self, request):
        """Prevent manual addition of history records (should be created via signals)."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Make history records read-only."""
        return False
