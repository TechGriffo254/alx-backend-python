# Django Signals, ORM & Advanced ORM Techniques

This project demonstrates advanced Django features including Event Listeners (Signals), ORM optimization, and caching strategies.

## Project Structure

```
Django-signals_orm-0x04/
└── messaging_app/
    ├── manage.py
    ├── messaging_app/
    │   ├── __init__.py
    │   ├── settings.py      # Task 5: Cache configuration
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── asgi.py
    ├── messaging/           # Main messaging app
    │   ├── models.py        # Tasks 0-4: All models
    │   ├── signals.py       # Tasks 0-2: Signal handlers
    │   ├── views.py         # Task 2: User deletion view
    │   ├── admin.py         # Admin configurations
    │   ├── apps.py          # App config with signal import
    │   ├── tests.py         # Comprehensive tests
    │   └── urls.py
    └── chats/               # Caching demonstration app
        ├── views.py         # Task 5: Cached views
        └── urls.py
```

## Features Implemented

### Task 0: Implement Signals for User Notifications ✅

**Files**: `messaging/models.py`, `messaging/signals.py`, `messaging/apps.py`, `messaging/admin.py`, `messaging/tests.py`

- Created `Message` model with sender, receiver, content, and timestamp fields
- Created `Notification` model linked to User and Message models
- Implemented `post_save` signal to automatically create notifications when messages are sent
- Signal distinguishes between new messages and replies

**Key Features**:
- Automatic notification creation via Django signals
- Notifications include message preview and sender information
- Different notification types for new messages vs replies

### Task 1: Create a Signal for Logging Message Edits ✅

**Files**: `messaging/models.py` (MessageHistory model, edited field)

- Added `edited` boolean field to Message model
- Created `MessageHistory` model to store edit history
- Implemented `pre_save` signal to capture old content before updates
- History includes timestamp and editor information

**Key Features**:
- Automatic history creation when messages are edited
- Preserves all previous versions of messages
- Only creates history when content actually changes
- Admin interface displays edit history

### Task 2: Use Signals for Deleting User-Related Data ✅

**Files**: `messaging/views.py` (delete_user view)

- Created `delete_user` view for account deletion
- Implemented `post_delete` signal on User model
- CASCADE foreign keys automatically clean up related data
- Signal provides logging and can be extended for custom cleanup logic

**Key Features**:
- Complete data cleanup when users delete accounts
- Messages, notifications, and history automatically removed
- Respects foreign key constraints
- Extensible for additional cleanup tasks

### Task 3: Leverage Advanced ORM Techniques for Threaded Conversations ✅

**Files**: `messaging/models.py` (parent_message field, get_all_replies method)

- Added `parent_message` self-referential foreign key to Message model
- Implemented threaded conversation views with optimized queries
- Used `select_related()` for foreign key optimization
- Used `prefetch_related()` for reverse foreign key and many-to-many optimization
- Recursive querying for nested replies

**Key Features**:
- Full threading support for conversations
- Optimized database queries reduce N+1 query problems
- Efficient loading of conversation trees
- Views demonstrate proper use of Django ORM optimization techniques

### Task 4: Custom ORM Manager for Unread Messages ✅

**Files**: `messaging/models.py` (UnreadMessagesManager, read field)

- Added `read` boolean field to Message model
- Created `UnreadMessagesManager` custom manager class
- Implemented `unread_for_user()` method with query optimization
- Used `.only()` to retrieve only necessary fields
- Integrated with views to display unread messages efficiently

**Key Features**:
- Custom manager provides clean API for filtering unread messages
- Query optimization with `select_related()` and `.only()`
- Reduces database load by limiting retrieved fields
- Reusable across multiple views

### Task 5: Implement Basic View Cache ✅

**Files**: `messaging_app/settings.py`, `chats/views.py`

- Configured Django cache backend (LocMemCache) in settings.py
- Applied `@cache_page(60)` decorator to conversation views
- Set 60-second cache timeout as required
- Cache automatically handles invalidation

**Key Features**:
- View-level caching reduces database queries
- Configurable cache timeout (60 seconds)
- Automatic cache key generation based on URL
- Simple decorator-based implementation

## Models

### Message
- **Fields**: sender, receiver, content, timestamp, edited, parent_message, read
- **Managers**: objects (default), unread (custom)
- **Features**: Threading, edit tracking, read status, optimized queries

### Notification
- **Fields**: user, message, notification_type, content, timestamp, read
- **Features**: Automatic creation via signals, read tracking

### MessageHistory
- **Fields**: message, old_content, edited_at, edited_by
- **Features**: Automatic creation via pre_save signal, complete edit audit trail

## Signals

### create_notification_on_new_message (post_save)
- Triggers when a new Message is created
- Creates a Notification for the receiver
- Handles both new messages and replies

### log_message_edit (pre_save)
- Triggers before a Message is updated
- Creates MessageHistory record with old content
- Only saves history if content actually changed

### delete_user_related_data (post_delete)
- Triggers when a User is deleted
- Provides logging and extensibility for cleanup
- Works with CASCADE foreign keys for automatic cleanup

## Setup Instructions

1. **Install Django** (if not already installed):
   ```bash
   pip install django
   ```

2. **Navigate to the project directory**:
   ```bash
   cd Django-signals_orm-0x04/messaging_app
   ```

3. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the admin interface**:
   - Navigate to http://127.0.0.1:8000/admin/
   - Login with superuser credentials
   - Create users and test the messaging system

## Testing

Run the comprehensive test suite:

```bash
python manage.py test messaging
```

### Test Coverage

- **MessageModelTest**: Basic model functionality
- **NotificationSignalTest**: Task 0 - Notification creation
- **MessageEditHistoryTest**: Task 1 - Edit history logging
- **UserDeletionTest**: Task 2 - Data cleanup on deletion
- **ThreadedConversationTest**: Task 3 - Threading and query optimization
- **UnreadMessagesManagerTest**: Task 4 - Custom manager functionality
- **IntegrationTest**: Complete message lifecycle

## Usage Examples

### Creating a Message
```python
from django.contrib.auth.models import User
from messaging.models import Message

sender = User.objects.get(username='alice')
receiver = User.objects.get(username='bob')

message = Message.objects.create(
    sender=sender,
    receiver=receiver,
    content='Hello Bob!'
)
# Notification is automatically created via signal
```

### Editing a Message
```python
message.content = 'Hello Bob! How are you?'
message.save()
# MessageHistory is automatically created via signal
# message.edited is set to True
```

### Getting Unread Messages
```python
# Using custom manager
unread = Message.unread.unread_for_user(user)
```

### Threaded Conversations
```python
# Create a reply
reply = Message.objects.create(
    sender=receiver,
    receiver=sender,
    content='I am fine, thanks!',
    parent_message=message
)

# Get all replies
replies = message.get_all_replies()
```

### Cached Views
```python
# Views with @cache_page(60) decorator automatically cache for 60 seconds
# Access /chats/conversations/ to see caching in action
```

## Cache Configuration

Located in `messaging_app/settings.py`:

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
```

## Admin Interface

All models are registered with enhanced admin interfaces:

- **Message**: View, filter, and search messages with threading support
- **Notification**: Manage user notifications
- **MessageHistory**: Read-only view of message edit history

## Best Practices Demonstrated

1. **Signal Handlers**:
   - Keep signal functions lean
   - Use @receiver decorator for clean registration
   - Separate business logic from signal handlers

2. **ORM Optimization**:
   - Use `select_related()` for foreign keys
   - Use `prefetch_related()` for reverse relationships
   - Implement custom managers for common queries
   - Use `.only()` to limit field retrieval

3. **Caching**:
   - Use appropriate cache timeouts
   - Cache view-level responses for performance
   - Clear or invalidate cache when data changes

4. **Testing**:
   - Comprehensive test coverage for all features
   - Test signals independently
   - Integration tests for complete workflows

## Performance Considerations

- **Database Indexes**: Added on frequently queried fields (receiver+read, sender+timestamp, parent_message)
- **Query Optimization**: Used select_related and prefetch_related throughout
- **Custom Managers**: Encapsulate optimized queries for reuse
- **Caching**: Reduces database load for frequently accessed views

## Repository Information

- **GitHub Repository**: alx-backend-python
- **Directory**: Django-signals_orm-0x04
- **Files**:
  - `messaging/models.py`
  - `messaging/signals.py`
  - `messaging/apps.py`
  - `messaging/admin.py`
  - `messaging/tests.py`
  - `messaging/views.py` (delete_user view)
  - `messaging_app/settings.py` (cache config)
  - `chats/views.py` (cached views)

## Author

ALX Backend Python Project - Django Signals, ORM & Advanced Techniques

## License

This project is part of the ALX Backend Python curriculum.
