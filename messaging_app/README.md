# Messaging App - Django REST Framework

A robust messaging application built with Django REST Framework that implements a complete messaging system with users, conversations, and messages.

## Project Structure

```
messaging_app/
├── messaging_app/          # Main project directory
│   ├── settings.py        # Project settings and configuration
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # WSGI configuration
├── chats/                 # Chats application
│   ├── models.py          # Data models (User, Conversation, Message)
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # ViewSets for API endpoints
│   ├── urls.py            # App-specific URL routing
│   ├── admin.py           # Django admin configuration
│   └── migrations/        # Database migrations
└── manage.py              # Django management script
```

## Features

### Models

1. **User Model** (extends AbstractUser)
   - UUID primary key
   - Email (unique)
   - Phone number
   - Role (guest, host, admin)
   - Timestamps

2. **Conversation Model**
   - UUID primary key
   - Many-to-many relationship with Users (participants)
   - Timestamps

3. **Message Model**
   - UUID primary key
   - Foreign key to User (sender)
   - Foreign key to Conversation
   - Message body (text)
   - Timestamps

### API Endpoints

All endpoints are prefixed with `/api/`

#### Users
- `GET /api/users/` - List all users
- `POST /api/users/` - Create a new user
- `GET /api/users/{id}/` - Retrieve a specific user
- `PUT /api/users/{id}/` - Update a user
- `DELETE /api/users/{id}/` - Delete a user

#### Conversations
- `GET /api/conversations/` - List all conversations
- `POST /api/conversations/` - Create a new conversation
- `GET /api/conversations/{id}/` - Retrieve a specific conversation with messages
- `PUT /api/conversations/{id}/` - Update a conversation
- `DELETE /api/conversations/{id}/` - Delete a conversation
- `POST /api/conversations/{id}/add_message/` - Add a message to a conversation

#### Messages
- `GET /api/messages/` - List all messages
- `POST /api/messages/` - Create a new message
- `GET /api/messages/{id}/` - Retrieve a specific message
- `PUT /api/messages/{id}/` - Update a message
- `DELETE /api/messages/{id}/` - Delete a message

## Installation

1. Install Django and Django REST Framework:
```bash
pip install django djangorestframework
```

2. Navigate to the project directory:
```bash
cd messaging_app
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Testing the API

You can test the API using:
- Django REST Framework's browsable API at `http://127.0.0.1:8000/api/`
- Postman or similar API testing tools
- curl commands

### Example: Create a Conversation

```bash
curl -X POST http://127.0.0.1:8000/api/conversations/ \
  -H "Content-Type: application/json" \
  -d '{
    "participant_ids": ["<user_id_1>", "<user_id_2>"]
  }'
```

### Example: Send a Message

```bash
curl -X POST http://127.0.0.1:8000/api/messages/ \
  -H "Content-Type: application/json" \
  -d '{
    "sender_id": "<user_id>",
    "conversation": "<conversation_id>",
    "message_body": "Hello, this is a test message!"
  }'
```

## Admin Interface

Access the Django admin interface at `http://127.0.0.1:8000/admin/` to manage:
- Users
- Conversations
- Messages

## Database

The project uses SQLite by default (db.sqlite3). For production, configure PostgreSQL or MySQL in `settings.py`.

## Key Implementation Details

### Serializers
- Nested serializers for displaying related data
- Separate read/write fields for relationships
- Custom `create` method in `ConversationSerializer` for handling many-to-many relationships

### ViewSets
- `ModelViewSet` for full CRUD operations
- Query optimization with `select_related` and `prefetch_related`
- Custom action `add_message` for conversation-specific message creation

### URL Routing
- `DefaultRouter` for automatic URL generation
- Modular routing with app-specific URLs included in main project

## Best Practices Followed

1. **UUID Primary Keys**: Enhanced security and scalability
2. **Related Names**: Clear reverse relationships (`sent_messages`, `conversations`, `messages`)
3. **Query Optimization**: Using `select_related` and `prefetch_related` to reduce database queries
4. **Proper Constraints**: Non-null fields, unique constraints, and proper foreign key relationships
5. **Ordering**: Messages ordered by `sent_at` for chronological display
6. **Django Admin**: Configured for easy data management
7. **RESTful Conventions**: Standard HTTP methods and URL patterns

## Project Requirements Completed

- ✅ Task 0: Django project setup with REST Framework
- ✅ Task 1: Data models defined with proper relationships
- ✅ Task 2: Serializers with nested relationships
- ✅ Task 3: ViewSets for API endpoints
- ✅ Task 4: URL routing configured
- ✅ Task 5: Application tested and running

## Repository

- **GitHub Repository**: alx-backend-python
- **Directory**: messaging_app
- **Branch**: master
