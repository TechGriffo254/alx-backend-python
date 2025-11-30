"""Models for the messaging application."""
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model extending Django's AbstractUser."""
    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    password = models.CharField(max_length=128, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='guest',
        null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string representation."""
        return f"{self.first_name} {self.last_name} ({self.email})"


class Conversation(models.Model):
    """Conversation model to track user conversations."""
    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    participants = models.ManyToManyField(
        User,
        related_name='conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string representation."""
        return f"Conversation {self.conversation_id}"


class Message(models.Model):
    """Message model for chat messages."""
    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    message_body = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options for Message model."""
        ordering = ['sent_at']

    def __str__(self):
        """Return string representation."""
        return f"Message from {self.sender} at {self.sent_at}"
