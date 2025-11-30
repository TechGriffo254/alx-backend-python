"""
Views for the messaging app.

Includes views for:
- Task 2: User deletion with automatic cleanup via signals
- Message management and display
- Threading conversation views (Task 3)
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages as django_messages
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Prefetch
from .models import Message, Notification, MessageHistory


@login_required
def delete_user(request):
    """
    Task 2: View to allow a user to delete their account.
    
    When a user is deleted, the post_delete signal automatically
    cleans up all related messages, notifications, and message histories
    due to CASCADE foreign key relationships.
    
    GET: Display confirmation page
    POST: Delete the user account
    """
    if request.method == 'POST':
        user = request.user
        username = user.username
        
        # Log out the user first
        from django.contrib.auth import logout
        logout(request)
        
        # Delete the user (this triggers the post_delete signal)
        user.delete()
        
        django_messages.success(
            request,
            f'Account {username} has been successfully deleted. All related data has been cleaned up.'
        )
        return redirect('home')  # Redirect to home or login page
    
    return render(request, 'messaging/delete_user_confirm.html')


@login_required
def inbox(request):
    """
    Display the user's inbox with all received messages.
    
    Uses the custom manager to show unread messages first,
    with optimized queries.
    """
    # Get unread messages using custom manager (Task 4)
    unread_messages = Message.unread.unread_for_user(request.user)
    
    # Get all messages with optimized loading
    all_messages = Message.objects.filter(
        receiver=request.user
    ).select_related('sender', 'parent_message').prefetch_related('replies')
    
    context = {
        'unread_messages': unread_messages,
        'all_messages': all_messages,
    }
    
    return render(request, 'messaging/inbox.html', context)


@login_required
def message_detail(request, message_id):
    """
    Task 3: Display a message with its threaded replies.
    
    Uses select_related and prefetch_related to optimize
    querying of messages and their replies.
    """
    # Get the message with optimized loading
    message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver', 'parent_message'),
        id=message_id
    )
    
    # Check permissions
    if request.user != message.sender and request.user != message.receiver:
        return HttpResponseForbidden("You don't have permission to view this message.")
    
    # Mark as read if the current user is the receiver
    if request.user == message.receiver:
        message.mark_as_read()
    
    # Get all replies with prefetch_related for optimization (Task 3)
    replies = Message.objects.filter(
        parent_message=message
    ).select_related('sender', 'receiver').prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
    )
    
    # Get message edit history (Task 1)
    history = MessageHistory.objects.filter(
        message=message
    ).select_related('edited_by').order_by('-edited_at')
    
    context = {
        'message': message,
        'replies': replies,
        'history': history,
    }
    
    return render(request, 'messaging/message_detail.html', context)


@login_required
def conversation_thread(request, message_id):
    """
    Task 3: Display a threaded conversation starting from a root message.
    
    Implements recursive querying using Django's ORM to fetch all replies
    in a threaded format with optimized database access.
    """
    # Get the root message
    root_message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver'),
        id=message_id
    )
    
    # Check permissions
    if request.user != root_message.sender and request.user != root_message.receiver:
        return HttpResponseForbidden("You don't have permission to view this conversation.")
    
    # Get all messages in the thread recursively
    # This uses prefetch_related to optimize the query
    messages_in_thread = Message.objects.filter(
        parent_message=root_message
    ).select_related('sender', 'receiver').prefetch_related(
        Prefetch(
            'replies',
            queryset=Message.objects.select_related('sender', 'receiver').prefetch_related('replies')
        )
    )
    
    context = {
        'root_message': root_message,
        'thread_messages': messages_in_thread,
    }
    
    return render(request, 'messaging/conversation_thread.html', context)


@login_required
def send_message(request):
    """Send a new message or reply to an existing message."""
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        content = request.POST.get('content')
        parent_message_id = request.POST.get('parent_message_id')
        
        receiver = get_object_or_404(User, id=receiver_id)
        
        parent_message = None
        if parent_message_id:
            parent_message = get_object_or_404(Message, id=parent_message_id)
        
        message = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            parent_message=parent_message
        )
        
        django_messages.success(request, 'Message sent successfully!')
        
        if parent_message:
            return redirect('message_detail', message_id=parent_message.id)
        else:
            return redirect('inbox')
    
    return render(request, 'messaging/send_message.html')


@login_required
def edit_message(request, message_id):
    """
    Edit a message (Task 1).
    
    When a message is edited, the pre_save signal automatically
    creates a MessageHistory record with the old content.
    """
    message = get_object_or_404(Message, id=message_id)
    
    # Only the sender can edit their message
    if request.user != message.sender:
        return HttpResponseForbidden("You can only edit your own messages.")
    
    if request.method == 'POST':
        new_content = request.POST.get('content')
        message.content = new_content
        message.save()  # This triggers the pre_save signal
        
        django_messages.success(request, 'Message updated successfully!')
        return redirect('message_detail', message_id=message.id)
    
    context = {
        'message': message,
    }
    
    return render(request, 'messaging/edit_message.html', context)


@login_required
def notifications(request):
    """Display all notifications for the current user."""
    user_notifications = Notification.objects.filter(
        user=request.user
    ).select_related('message', 'message__sender').order_by('-timestamp')
    
    context = {
        'notifications': user_notifications,
    }
    
    return render(request, 'messaging/notifications.html', context)


@login_required
def mark_notification_read(request, notification_id):
    """Mark a notification as read."""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.mark_as_read()
    
    return JsonResponse({'status': 'success'})
