"""
URL configuration for the messaging app.
"""

from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    # Task 2: User deletion
    path('delete-account/', views.delete_user, name='delete_user'),
    
    # Message views
    path('inbox/', views.inbox, name='inbox'),
    path('message/<int:message_id>/', views.message_detail, name='message_detail'),
    path('send/', views.send_message, name='send_message'),
    path('edit/<int:message_id>/', views.edit_message, name='edit_message'),
    
    # Task 3: Threaded conversations
    path('thread/<int:message_id>/', views.conversation_thread, name='conversation_thread'),
    
    # Notifications
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
]
