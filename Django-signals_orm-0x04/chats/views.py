"""
Views for the chats app with caching implementation.

Task 5: Implements basic view-level caching using Django's cache_page decorator.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from messaging.models import Message


@login_required
@cache_page(60)  # Cache for 60 seconds as required by Task 5
def conversation_list(request):
    """
    Task 5: Display a list of messages in a conversation with caching.
    
    This view is cached for 60 seconds using the @cache_page decorator.
    This reduces database load by serving cached responses for repeated
    requests within the cache timeout period.
    
    The cache key is automatically generated based on the URL and user session.
    """
    # Get all messages involving the current user
    messages = Message.objects.filter(
        receiver=request.user
    ).select_related('sender', 'receiver').order_by('-timestamp')[:50]
    
    context = {
        'messages': messages,
        'cache_timeout': 60,  # Display cache info to user
    }
    
    return render(request, 'chats/conversation_list.html', context)


@login_required
@cache_page(60)
def message_list(request):
    """
    Alternative cached view for displaying messages.
    
    This demonstrates basic view-level caching with a 60-second timeout.
    Multiple views can use caching to improve performance across the app.
    """
    # Get messages with optimized queries
    sent_messages = Message.objects.filter(
        sender=request.user
    ).select_related('receiver').order_by('-timestamp')[:25]
    
    received_messages = Message.objects.filter(
        receiver=request.user
    ).select_related('sender').order_by('-timestamp')[:25]
    
    context = {
        'sent_messages': sent_messages,
        'received_messages': received_messages,
    }
    
    return render(request, 'chats/message_list.html', context)


def home(request):
    """Simple home view without caching."""
    return render(request, 'chats/home.html')
