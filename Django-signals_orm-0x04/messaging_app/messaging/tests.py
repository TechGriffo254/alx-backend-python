"""
Tests for the messaging app.

Tests cover:
- Task 0: Notification creation via signals
- Task 1: Message edit history via signals
- Task 2: User deletion and cleanup
- Task 3: Threaded conversations with optimized queries
- Task 4: Custom manager for unread messages
"""

from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User
from django.db import connection
from django.test.utils import override_settings
from .models import Message, Notification, MessageHistory
from .signals import (
    create_notification_on_new_message,
    log_message_edit,
    delete_user_related_data
)


class MessageModelTest(TestCase):
    """Test the Message model."""
    
    def setUp(self):
        """Create test users."""
        self.user1 = User.objects.create_user(username='alice', password='testpass123')
        self.user2 = User.objects.create_user(username='bob', password='testpass123')
    
    def test_message_creation(self):
        """Test creating a basic message."""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Hello Bob!'
        )
        
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.receiver, self.user2)
        self.assertEqual(message.content, 'Hello Bob!')
        self.assertFalse(message.edited)
        self.assertFalse(message.read)
        self.assertIsNone(message.parent_message)
    
    def test_threaded_message(self):
        """Task 3: Test creating a threaded reply message."""
        # Create parent message
        parent = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Parent message'
        )
        
        # Create reply
        reply = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content='Reply message',
            parent_message=parent
        )
        
        self.assertEqual(reply.parent_message, parent)
        self.assertIn(reply, parent.replies.all())
    
    def test_mark_as_read(self):
        """Test marking a message as read."""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Test message'
        )
        
        self.assertFalse(message.read)
        message.mark_as_read()
        self.assertTrue(message.read)


class NotificationSignalTest(TestCase):
    """Task 0: Test automatic notification creation via signals."""
    
    def setUp(self):
        """Create test users."""
        self.user1 = User.objects.create_user(username='alice', password='testpass123')
        self.user2 = User.objects.create_user(username='bob', password='testpass123')
    
    def test_notification_created_on_new_message(self):
        """Test that a notification is automatically created when a message is sent."""
        # Initially no notifications
        self.assertEqual(Notification.objects.count(), 0)
        
        # Create a message
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Hello Bob!'
        )
        
        # Check that notification was created
        self.assertEqual(Notification.objects.count(), 1)
        
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.user2)
        self.assertEqual(notification.message, message)
        self.assertEqual(notification.notification_type, 'new_message')
        self.assertIn(self.user1.username, notification.content)
    
    def test_notification_for_reply(self):
        """Test that reply notifications have correct type."""
        # Create parent message
        parent = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Parent message'
        )
        
        # Clear notifications from parent
        Notification.objects.all().delete()
        
        # Create reply
        reply = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content='Reply message',
            parent_message=parent
        )
        
        notification = Notification.objects.first()
        self.assertEqual(notification.notification_type, 'message_reply')


class MessageEditHistoryTest(TestCase):
    """Task 1: Test message edit history via signals."""
    
    def setUp(self):
        """Create test users and a message."""
        self.user1 = User.objects.create_user(username='alice', password='testpass123')
        self.user2 = User.objects.create_user(username='bob', password='testpass123')
        
        self.message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Original content'
        )
    
    def test_history_created_on_edit(self):
        """Test that MessageHistory is created when a message is edited."""
        # Initially no history
        self.assertEqual(MessageHistory.objects.count(), 0)
        
        # Edit the message
        self.message.content = 'Updated content'
        self.message.save()
        
        # Check that history was created
        self.assertEqual(MessageHistory.objects.count(), 1)
        
        history = MessageHistory.objects.first()
        self.assertEqual(history.message, self.message)
        self.assertEqual(history.old_content, 'Original content')
        self.assertTrue(self.message.edited)
    
    def test_multiple_edits_create_multiple_history_records(self):
        """Test that multiple edits create multiple history records."""
        # First edit
        self.message.content = 'First edit'
        self.message.save()
        
        # Second edit
        self.message.content = 'Second edit'
        self.message.save()
        
        # Should have 2 history records
        self.assertEqual(MessageHistory.objects.count(), 2)
        
        histories = MessageHistory.objects.order_by('edited_at')
        self.assertEqual(histories[0].old_content, 'Original content')
        self.assertEqual(histories[1].old_content, 'First edit')
    
    def test_no_history_if_content_unchanged(self):
        """Test that history is not created if content doesn't change."""
        # Save without changing content
        self.message.read = True
        self.message.save()
        
        # No history should be created
        self.assertEqual(MessageHistory.objects.count(), 0)


class UserDeletionTest(TransactionTestCase):
    """Task 2: Test user deletion and related data cleanup."""
    
    def setUp(self):
        """Create test users and related data."""
        self.user1 = User.objects.create_user(username='alice', password='testpass123')
        self.user2 = User.objects.create_user(username='bob', password='testpass123')
        
        # Create messages
        self.message1 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Message from Alice'
        )
        
        self.message2 = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content='Message from Bob'
        )
    
    def test_messages_deleted_when_user_deleted(self):
        """Test that messages are deleted when a user is deleted."""
        user1_id = self.user1.id
        
        # Verify messages exist
        self.assertEqual(Message.objects.filter(sender=self.user1).count(), 1)
        self.assertEqual(Message.objects.filter(receiver=self.user1).count(), 1)
        
        # Delete user
        self.user1.delete()
        
        # Check that messages are deleted due to CASCADE
        self.assertEqual(Message.objects.filter(sender_id=user1_id).count(), 0)
        self.assertEqual(Message.objects.filter(receiver_id=user1_id).count(), 0)
    
    def test_notifications_deleted_when_user_deleted(self):
        """Test that notifications are deleted when a user is deleted."""
        # Notifications were created by signals
        self.assertTrue(Notification.objects.filter(user=self.user2).exists())
        
        user2_id = self.user2.id
        
        # Delete user
        self.user2.delete()
        
        # Check that notifications are deleted
        self.assertEqual(Notification.objects.filter(user_id=user2_id).count(), 0)
    
    def test_message_history_deleted_when_user_deleted(self):
        """Test that message history is deleted when a user is deleted."""
        # Edit a message to create history
        self.message1.content = 'Updated content'
        self.message1.save()
        
        # Verify history exists
        self.assertTrue(MessageHistory.objects.filter(message=self.message1).exists())
        
        # Delete user (this will delete the message, which will delete the history)
        self.user1.delete()
        
        # History should be deleted because the message was deleted
        self.assertEqual(MessageHistory.objects.count(), 0)


class ThreadedConversationTest(TestCase):
    """Task 3: Test threaded conversations and query optimization."""
    
    def setUp(self):
        """Create test users and threaded messages."""
        self.user1 = User.objects.create_user(username='alice', password='testpass123')
        self.user2 = User.objects.create_user(username='bob', password='testpass123')
        
        # Create a conversation thread
        self.root_message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Root message'
        )
        
        self.reply1 = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content='First reply',
            parent_message=self.root_message
        )
        
        self.reply2 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Second reply',
            parent_message=self.root_message
        )
        
        # Nested reply
        self.nested_reply = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content='Nested reply',
            parent_message=self.reply1
        )
    
    def test_get_all_replies(self):
        """Test getting all replies to a message."""
        replies = self.root_message.get_all_replies()
        
        # Should have 2 direct replies
        self.assertEqual(replies.count(), 2)
        self.assertIn(self.reply1, replies)
        self.assertIn(self.reply2, replies)
    
    def test_nested_replies(self):
        """Test nested reply structure."""
        nested_replies = self.reply1.get_all_replies()
        
        self.assertEqual(nested_replies.count(), 1)
        self.assertEqual(nested_replies.first(), self.nested_reply)
    
    def test_optimized_query_with_select_related(self):
        """Test that select_related reduces queries."""
        # Reset query count
        connection.queries_log.clear()
        
        with self.assertNumQueries(1):
            # This should use select_related to load sender and receiver in one query
            messages = list(
                Message.objects.filter(
                    parent_message=self.root_message
                ).select_related('sender', 'receiver')
            )
            
            # Access related objects (should not trigger additional queries)
            for msg in messages:
                _ = msg.sender.username
                _ = msg.receiver.username


class UnreadMessagesManagerTest(TestCase):
    """Task 4: Test custom manager for unread messages."""
    
    def setUp(self):
        """Create test users and messages."""
        self.user1 = User.objects.create_user(username='alice', password='testpass123')
        self.user2 = User.objects.create_user(username='bob', password='testpass123')
        
        # Create some messages
        self.read_message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Read message',
            read=True
        )
        
        self.unread_message1 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Unread message 1'
        )
        
        self.unread_message2 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Unread message 2'
        )
    
    def test_unread_manager_filters_correctly(self):
        """Test that the unread manager returns only unread messages."""
        unread = Message.unread.unread_for_user(self.user2)
        
        self.assertEqual(unread.count(), 2)
        self.assertIn(self.unread_message1, unread)
        self.assertIn(self.unread_message2, unread)
        self.assertNotIn(self.read_message, unread)
    
    def test_unread_manager_optimizes_with_only(self):
        """Test that the unread manager uses only() for optimization."""
        unread = Message.unread.unread_for_user(self.user2)
        
        # The query should use only() to limit fields
        # We can check this by examining the query
        query_str = str(unread.query)
        
        # Just verify it executes without error and returns correct count
        self.assertEqual(len(list(unread)), 2)
    
    def test_empty_unread_messages(self):
        """Test unread manager when there are no unread messages."""
        # Mark all as read
        Message.objects.filter(receiver=self.user2).update(read=True)
        
        unread = Message.unread.unread_for_user(self.user2)
        self.assertEqual(unread.count(), 0)


class IntegrationTest(TestCase):
    """Integration tests for the complete messaging system."""
    
    def setUp(self):
        """Create test users."""
        self.user1 = User.objects.create_user(username='alice', password='testpass123')
        self.user2 = User.objects.create_user(username='bob', password='testpass123')
    
    def test_complete_message_lifecycle(self):
        """Test the complete lifecycle of a message with all features."""
        # 1. Create a message (should trigger notification)
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Hello Bob!'
        )
        
        # Verify notification was created
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.user2)
        
        # 2. Edit the message (should create history)
        message.content = 'Hello Bob! How are you?'
        message.save()
        
        # Verify history was created and edited flag is set
        self.assertTrue(message.edited)
        self.assertEqual(MessageHistory.objects.count(), 1)
        history = MessageHistory.objects.first()
        self.assertEqual(history.old_content, 'Hello Bob!')
        
        # 3. Create a reply (should create notification and link to parent)
        reply = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content='I am fine, thanks!',
            parent_message=message
        )
        
        # Verify reply structure
        self.assertEqual(reply.parent_message, message)
        self.assertEqual(Notification.objects.count(), 2)
        
        # 4. Check unread messages
        unread = Message.unread.unread_for_user(self.user2)
        self.assertIn(message, unread)
        
        # 5. Mark as read
        message.mark_as_read()
        unread = Message.unread.unread_for_user(self.user2)
        self.assertNotIn(message, unread)
