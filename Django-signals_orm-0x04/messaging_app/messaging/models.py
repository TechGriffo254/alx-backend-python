"""
Models for the messaging app.

This module contains all the models for the messaging application including:
- Message: Main message model with threading support, edit tracking, and read status
- Notification: User notifications for new messages
- MessageHistory: Historical records of message edits
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UnreadMessagesManager(models.Manager):
    """
    Custom manager for filtering unread messages.
    
    Task 4: Custom ORM Manager for Unread Messages
    This manager provides an optimized way to retrieve unread messages
    for a specific user using only() to limit fields retrieved.
    """
    
    def unread_for_user(self, user):
        """
        Get all unread messages for a specific user.
        
        Args:
            user: The User instance to filter messages for
            
        Returns:
            QuerySet of unread Message instances with optimized field loading
        """
        return self.filter(
            receiver=user,
            read=False
        ).select_related('sender', 'parent_message').only(
            'id',
            'sender__username',
            'sender__email',
            'content',
            'timestamp',
            'read',
            'parent_message__id'
        )


class Message(models.Model):
    """
    Message model representing messages between users.
    
    Features:
    - Task 0: Basic message structure with sender/receiver
    - Task 1: Edit tracking with edited field
    - Task 3: Threading with parent_message self-referential FK
    - Task 4: Read status tracking with read field and custom manager
    """
    
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text='User who sent the message'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages',
        help_text='User who receives the message'
    )
    content = models.TextField(
        help_text='The message content'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text='When the message was created'
    )
    edited = models.BooleanField(
        default=False,
        help_text='Whether the message has been edited (Task 1)'
    )
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        help_text='Parent message for threading conversations (Task 3)'
    )
    read = models.BooleanField(
        default=False,
        help_text='Whether the message has been read by the receiver (Task 4)'
    )
    
    # Default manager
    objects = models.Manager()
    
    # Custom manager for unread messages (Task 4)
    unread = UnreadMessagesManager()
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['receiver', 'read']),
            models.Index(fields=['sender', 'timestamp']),
            models.Index(fields=['parent_message']),
        ]
    
    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} at {self.timestamp}"
    
    def get_all_replies(self):
        """
        Recursively get all replies to this message (Task 3).
        
        Returns:
            QuerySet of all replies with optimized loading
        """
        return Message.objects.filter(
            parent_message=self
        ).select_related('sender', 'receiver').prefetch_related('replies')
    
    def mark_as_read(self):
        """Mark this message as read."""
        if not self.read:
            self.read = True
            self.save(update_fields=['read'])


class Notification(models.Model):
    """
    Notification model for user notifications.
    
    Task 0: Automatically created via post_save signal when a new message is sent.
    Links to both User and Message models.
    """
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text='User who receives the notification'
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text='The message that triggered this notification'
    )
    notification_type = models.CharField(
        max_length=50,
        default='new_message',
        help_text='Type of notification (e.g., new_message, message_reply)'
    )
    content = models.TextField(
        help_text='Notification message content'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text='When the notification was created'
    )
    read = models.BooleanField(
        default=False,
        help_text='Whether the notification has been read'
    )
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'read']),
        ]
    
    def __str__(self):
        return f"Notification for {self.user.username}: {self.notification_type}"
    
    def mark_as_read(self):
        """Mark this notification as read."""
        if not self.read:
            self.read = True
            self.save(update_fields=['read'])


class MessageHistory(models.Model):
    """
    MessageHistory model for tracking message edits.
    
    Task 1: Stores the old content of a message before it's edited.
    Created automatically via pre_save signal.
    """
    
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='history',
        help_text='The message that was edited'
    )
    old_content = models.TextField(
        help_text='The previous content before the edit'
    )
    edited_at = models.DateTimeField(
        auto_now_add=True,
        help_text='When the edit occurred'
    )
    edited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='User who edited the message'
    )
    
    class Meta:
        ordering = ['-edited_at']
        verbose_name_plural = 'Message histories'
        indexes = [
            models.Index(fields=['message', 'edited_at']),
        ]
    
    def __str__(self):
        return f"History for message {self.message.id} edited at {self.edited_at}"
