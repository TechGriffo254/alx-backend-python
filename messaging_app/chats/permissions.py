"""Custom permission classes for the messaging application."""
from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    
    This permission ensures that:
    - Only authenticated users can access the API
    - Only participants in a conversation can view, send, update, and delete messages
    - Users can only access conversations they are part of
    """
    
    message = "You must be a participant of this conversation to access it."
    
    def has_permission(self, request, view):
        """
        Check if user is authenticated.
        """
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Check if user is a participant of the conversation.
        
        For Message objects, check if user is participant of the conversation.
        For Conversation objects, check if user is in the participants list.
        """
        # Import here to avoid circular imports
        from .models import Message, Conversation
        
        # If the object is a Message, check the conversation
        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()
        
        # If the object is a Conversation, check participants directly
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()
        
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Read permissions are allowed to any authenticated user.
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Read permissions are allowed for any request,
        Write permissions are only allowed to the owner.
        """
        # Read permissions for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for owner
        # For messages, check if user is the sender
        if hasattr(obj, 'sender'):
            return obj.sender == request.user
        
        # For users, check if it's the same user
        if hasattr(obj, 'user_id'):
            return obj.user_id == request.user.user_id
        
        return False


class IsMessageSender(permissions.BasePermission):
    """
    Custom permission to only allow the sender of a message to edit or delete it.
    """
    
    message = "You can only edit or delete your own messages."
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the sender of the message.
        """
        # Read permissions for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write/Delete permissions only for the sender
        return obj.sender == request.user


class IsAdminOrOwner(permissions.BasePermission):
    """
    Custom permission to allow admins full access and users access to their own data.
    """
    
    def has_permission(self, request, view):
        """
        Check if user is authenticated.
        """
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Allow admins full access and users access to their own data.
        """
        # Admin users have full access
        if request.user.role == 'admin' or request.user.is_staff:
            return True
        
        # Users can access their own data
        if hasattr(obj, 'user_id'):
            return obj.user_id == request.user.user_id
        
        if hasattr(obj, 'sender'):
            return obj.sender == request.user
        
        return False
