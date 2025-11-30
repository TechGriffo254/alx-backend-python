# Setup and Testing Guide

## Quick Start

### 1. Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### 2. Installation Steps

```powershell
# Navigate to the project directory
cd c:\Users\Admin\workspaces\alx-backend-python\Django-signals_orm-0x04

# Create a virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Navigate to the Django project
cd messaging_app
```

### 3. Database Setup

```powershell
# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### 4. Create Superuser

```powershell
# Create an admin user
python manage.py createsuperuser

# Follow the prompts to enter:
# - Username
# - Email (optional)
# - Password
```

### 5. Run the Server

```powershell
python manage.py runserver
```

The server will start at http://127.0.0.1:8000/

## Testing Each Task

### Task 0: Test Notification Signals

1. Access Django Admin: http://127.0.0.1:8000/admin/
2. Login with your superuser credentials
3. Create at least 2 users (Users → Add user)
4. Create a message (Messages → Add message):
   - Select a sender
   - Select a receiver
   - Enter content
   - Save
5. Check Notifications section - a notification should be automatically created!

**Expected Result**: A notification is automatically created for the receiver when a message is sent.

### Task 1: Test Message Edit History

1. In Django Admin, go to Messages
2. Find an existing message and click to edit it
3. Change the content and save
4. Go to Message Histories section
5. You should see a record of the old content!

**Expected Result**: 
- Message shows "Edited: Yes"
- MessageHistory record contains the previous content
- Timestamp shows when the edit occurred

### Task 2: Test User Deletion and Cleanup

1. Create a test user and send/receive some messages
2. Check that messages, notifications, and history exist
3. Delete the user from Django Admin
4. Verify that all related data is deleted

**Alternative - Use the view**:
```powershell
# The delete_user view is available at /messaging/delete-account/
# (requires login)
```

**Expected Result**: All messages, notifications, and history associated with the deleted user are removed.

### Task 3: Test Threaded Conversations

1. Create a parent message in Django Admin
2. Create a reply by setting the "Parent message" field to the parent message
3. View the message detail page to see threading
4. Check the conversation thread view

**Expected Result**:
- Replies are linked to parent messages
- Thread view shows the conversation hierarchy
- Optimized queries use select_related/prefetch_related

### Task 4: Test Custom Unread Messages Manager

Run the following in Django shell:

```powershell
python manage.py shell
```

```python
from django.contrib.auth.models import User
from messaging.models import Message

# Get a user
user = User.objects.get(username='your_username')

# Get unread messages using custom manager
unread = Message.unread.unread_for_user(user)
print(f"Unread messages: {unread.count()}")

# Mark one as read
if unread.exists():
    msg = unread.first()
    msg.mark_as_read()
    
# Check again
unread = Message.unread.unread_for_user(user)
print(f"Unread messages now: {unread.count()}")
```

**Expected Result**: Custom manager correctly filters unread messages and optimizes queries.

### Task 5: Test View Caching

1. Open your browser and navigate to: http://127.0.0.1:8000/chats/conversations/
2. Note the current time
3. Refresh the page multiple times within 60 seconds
4. The data should be served from cache (faster load)
5. Wait more than 60 seconds and refresh - data updates from database

**To verify caching is working**:

```powershell
# In Django shell
python manage.py shell
```

```python
from django.core.cache import cache

# Check if cache is working
cache.set('test_key', 'test_value', 30)
print(cache.get('test_key'))  # Should print: test_value

# Check cache configuration
from django.conf import settings
print(settings.CACHES)
```

**Expected Result**: Views with @cache_page(60) decorator cache responses for 60 seconds.

## Running Automated Tests

### Run All Tests

```powershell
python manage.py test messaging
```

### Run Specific Test Classes

```powershell
# Test Task 0 - Notifications
python manage.py test messaging.tests.NotificationSignalTest

# Test Task 1 - Edit History
python manage.py test messaging.tests.MessageEditHistoryTest

# Test Task 2 - User Deletion
python manage.py test messaging.tests.UserDeletionTest

# Test Task 3 - Threading
python manage.py test messaging.tests.ThreadedConversationTest

# Test Task 4 - Custom Manager
python manage.py test messaging.tests.UnreadMessagesManagerTest
```

### Expected Test Output

```
Found X tests for 'messaging'
System check identified no issues (0 silenced).
..........
----------------------------------------------------------------------
Ran X tests in X.XXXs

OK
```

## Verification Checklist

### Task 0: Signals for User Notifications ✅
- [ ] Message model exists with sender, receiver, content, timestamp
- [ ] Notification model exists linked to User and Message
- [ ] post_save signal creates notification on new message
- [ ] Signal distinguishes between new messages and replies
- [ ] Tests pass: NotificationSignalTest

### Task 1: Signal for Logging Message Edits ✅
- [ ] Message model has edited field
- [ ] MessageHistory model exists
- [ ] pre_save signal creates history record before update
- [ ] History shows old content with timestamp
- [ ] Tests pass: MessageEditHistoryTest

### Task 2: Signals for User Deletion ✅
- [ ] delete_user view exists in messaging/views.py
- [ ] post_delete signal on User model
- [ ] CASCADE foreign keys clean up related data
- [ ] All messages, notifications, history deleted with user
- [ ] Tests pass: UserDeletionTest

### Task 3: Advanced ORM for Threading ✅
- [ ] Message model has parent_message field
- [ ] Views use select_related and prefetch_related
- [ ] Recursive querying for threaded replies
- [ ] Optimized database queries
- [ ] Tests pass: ThreadedConversationTest

### Task 4: Custom ORM Manager ✅
- [ ] Message model has read field
- [ ] UnreadMessagesManager implemented
- [ ] unread_for_user() method with optimization
- [ ] Uses .only() to limit fields
- [ ] Tests pass: UnreadMessagesManagerTest

### Task 5: Basic View Cache ✅
- [ ] CACHES configured in settings.py with LocMemCache
- [ ] @cache_page(60) decorator on views in chats/views.py
- [ ] 60-second timeout as required
- [ ] Views serve cached responses

## Troubleshooting

### Issue: Migrations not applying
```powershell
python manage.py makemigrations --empty messaging
python manage.py migrate --run-syncdb
```

### Issue: Signals not firing
- Check that signals.py is imported in apps.py
- Verify ready() method in MessagingConfig calls import messaging.signals

### Issue: Tests failing
```powershell
# Run tests with verbose output
python manage.py test messaging --verbosity=2

# Run a single test method
python manage.py test messaging.tests.NotificationSignalTest.test_notification_created_on_new_message
```

### Issue: Cache not working
- Verify CACHES configuration in settings.py
- Check that views have @cache_page decorator
- Clear cache: python manage.py shell → from django.core.cache import cache → cache.clear()

### Issue: Import errors
```powershell
# Reinstall Django
pip uninstall django
pip install django>=4.2,<5.0
```

## File Checklist for Submission

Ensure all required files exist:

```
Django-signals_orm-0x04/
├── README.md
├── requirements.txt
└── messaging_app/
    ├── manage.py
    ├── messaging_app/
    │   └── settings.py (with CACHES configuration)
    ├── messaging/
    │   ├── models.py (all 3 models)
    │   ├── signals.py (all signal handlers)
    │   ├── apps.py (with ready() method)
    │   ├── admin.py (all model registrations)
    │   ├── tests.py (comprehensive tests)
    │   └── views.py (including delete_user)
    └── chats/
        └── views.py (cached views with @cache_page(60))
```

## Manual QA Review

Before requesting a manual review:

1. ✅ All tasks completed (0-5)
2. ✅ All tests passing
3. ✅ Django server runs without errors
4. ✅ Admin interface accessible
5. ✅ README.md documents all features
6. ✅ Code follows Django best practices
7. ✅ Signals properly registered and firing
8. ✅ ORM optimizations in place
9. ✅ Cache configuration correct
10. ✅ All required files present

## Additional Resources

- Django Signals Documentation: https://docs.djangoproject.com/en/4.2/topics/signals/
- Django ORM Documentation: https://docs.djangoproject.com/en/4.2/topics/db/queries/
- Django Caching Documentation: https://docs.djangoproject.com/en/4.2/topics/cache/
- Query Optimization: https://docs.djangoproject.com/en/4.2/topics/db/optimization/

## Support

If you encounter any issues:
1. Check this guide's troubleshooting section
2. Review the Django documentation
3. Check that all dependencies are installed
4. Verify Python version compatibility

Good luck with your manual QA review! 🚀
