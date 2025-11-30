"""
URL configuration for the chats app.

Task 5: Includes cached views.
"""

from django.urls import path
from . import views

app_name = 'chats'

urlpatterns = [
    path('', views.home, name='home'),
    # Task 5: Cached views with 60-second timeout
    path('conversations/', views.conversation_list, name='conversation_list'),
    path('messages/', views.message_list, name='message_list'),
]
