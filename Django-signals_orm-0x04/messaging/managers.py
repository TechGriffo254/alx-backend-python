"""
Custom managers for the messaging app.

This module contains custom Django model managers for optimized queries.
"""

from django.db import models


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
