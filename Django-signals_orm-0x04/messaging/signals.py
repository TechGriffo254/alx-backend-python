"""
Django signals for the messaging app.

This module contains signal handlers for:
- Task 0: Automatic notification creation when new messages are sent
- Task 1: Logging message edits to MessageHistory
- Task 2: Cleaning up related data when users are deleted
"""

from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    """
    Task 0: Signal handler to create a notification when a new message is sent.
    
    This signal listens to the post_save event on the Message model and
    automatically creates a Notification for the receiving user.
    
    Args:
        sender: The Message model class
        instance: The Message instance that was saved
        created: Boolean indicating if this is a new instance
        **kwargs: Additional keyword arguments
    """
    if created:
        # Determine notification type based on whether it's a reply
        notification_type = 'message_reply' if instance.parent_message else 'new_message'
        
        # Create notification content
        if instance.parent_message:
            content = f"{instance.sender.username} replied to your message: {instance.content[:50]}..."
        else:
            content = f"New message from {instance.sender.username}: {instance.content[:50]}..."
        
        # Create the notification
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            notification_type=notification_type,
            content=content
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Task 1: Signal handler to log message edits before they are saved.
    
    This signal listens to the pre_save event on the Message model and
    saves the old content to MessageHistory before the message is updated.
    
    Args:
        sender: The Message model class
        instance: The Message instance being saved
        **kwargs: Additional keyword arguments
    """
    # Only process if the message already exists (not a new creation)
    if instance.pk:
        try:
            # Get the old version of the message from the database
            old_message = Message.objects.get(pk=instance.pk)
            
            # Check if the content has actually changed
            if old_message.content != instance.content:
                # Mark the message as edited
                instance.edited = True
                
                # Create a history record with the old content
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content,
                    edited_by=instance.sender  # Assuming sender is editing their own message
                )
        except Message.DoesNotExist:
            # This shouldn't happen, but we handle it gracefully
            pass


@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    """
    Task 2: Signal handler to clean up related data when a user is deleted.
    
    This signal listens to the post_delete event on the User model and
    explicitly deletes all messages, notifications, and message histories 
    associated with the user.
    
    Args:
        sender: The User model class
        instance: The User instance that was deleted
        **kwargs: Additional keyword arguments
    """
    # Explicitly delete all messages sent by this user
    Message.objects.filter(sender=instance).delete()
    
    # Explicitly delete all messages received by this user
    Message.objects.filter(receiver=instance).delete()
    
    # Explicitly delete all notifications for this user
    Notification.objects.filter(user=instance).delete()
    
    # Message histories are automatically deleted when messages are deleted
    # due to CASCADE foreign key relationship
    
    # Log the deletion for auditing purposes
    print(f"Cleaning up data for deleted user: {instance.username}")


@receiver(pre_delete, sender=User)
def cleanup_user_data_before_delete(sender, instance, **kwargs):
    """
    Task 2: Clean up user-related data before user deletion.
    
    This pre_delete signal explicitly removes all messages, notifications,
    and related data before the user is deleted. This demonstrates explicit
    cleanup using Message.objects.filter().delete() pattern.
    
    Args:
        sender: The User model class
        instance: The User instance about to be deleted
        **kwargs: Additional keyword arguments
    """
    # Explicitly delete all messages where user is sender
    Message.objects.filter(sender=instance).delete()
    
    # Explicitly delete all messages where user is receiver  
    Message.objects.filter(receiver=instance).delete()
    
    # Delete all notifications for this user
    Notification.objects.filter(user=instance).delete()
    
    print(f"Pre-delete cleanup completed for user: {instance.username}")
