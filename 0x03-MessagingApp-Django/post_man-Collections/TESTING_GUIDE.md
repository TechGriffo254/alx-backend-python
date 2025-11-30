# Postman Testing Guide - Messaging App API

## Overview
This guide provides step-by-step instructions for testing the Messaging App API using Postman, including authentication, permissions, pagination, and filtering features.

## Prerequisites
1. Postman installed (Download from https://www.postman.com/downloads/)
2. Django development server running on http://localhost:8000
3. Database migrations applied

## Setup Instructions

### 1. Start the Django Server
```powershell
cd "c:\Users\Admin\Downloads\New folder\alx-backend-python\messaging_app"
"C:/Users/Admin/Downloads/New folder/.venv/Scripts/python.exe" manage.py makemigrations
"C:/Users/Admin/Downloads/New folder/.venv/Scripts/python.exe" manage.py migrate
"C:/Users/Admin/Downloads/New folder/.venv/Scripts/python.exe" manage.py runserver
```

### 2. Import Postman Collection
1. Open Postman
2. Click "Import" button
3. Select the file: `post_man-Collections/MessagingApp_API_Collection.json`
4. The collection will be imported with all endpoints and tests

### 3. Configure Environment Variables
The collection uses the following variables (auto-set during testing):
- `base_url`: http://localhost:8000 (default)
- `access_token`: JWT access token (auto-set after login/register)
- `refresh_token`: JWT refresh token (auto-set after login/register)
- `user_id`: Current user ID (auto-set after login/register)
- `conversation_id`: Created conversation ID (auto-set)
- `message_id`: Created message ID (auto-set)

## Testing Workflow

### Phase 1: Authentication Testing

#### Test 1: User Registration
**Endpoint:** POST `/api/auth/register/`

**Request Body:**
```json
{
    "username": "testuser1",
    "email": "testuser1@example.com",
    "password": "SecurePass123!",
    "first_name": "Test",
    "last_name": "User",
    "phone_number": "+1234567890",
    "role": "guest"
}
```

**Expected Response (201 Created):**
```json
{
    "user": {
        "user_id": "uuid-here",
        "username": "testuser1",
        "email": "testuser1@example.com",
        ...
    },
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "message": "User registered successfully"
}
```

**What to Verify:**
✅ Status code is 201
✅ Response contains user data
✅ Access and refresh tokens are returned
✅ Tokens are automatically saved to collection variables

#### Test 2: User Login
**Endpoint:** POST `/api/auth/login/`

**Request Body:**
```json
{
    "username": "testuser1",
    "password": "SecurePass123!"
}
```

**Expected Response (200 OK):**
```json
{
    "user": {...},
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "message": "Login successful"
}
```

**What to Verify:**
✅ Status code is 200
✅ Valid JWT tokens returned
✅ User information matches registered user

#### Test 3: Token Refresh
**Endpoint:** POST `/api/auth/token/refresh/`

**Request Body:**
```json
{
    "refresh": "{{refresh_token}}"
}
```

**Expected Response (200 OK):**
```json
{
    "access": "new-access-token",
    "refresh": "new-refresh-token"
}
```

**What to Verify:**
✅ New access token is generated
✅ New refresh token is returned (with rotation enabled)

#### Test 4: Unauthorized Access
**Endpoint:** GET `/api/conversations/` (without Authorization header)

**Expected Response (401 Unauthorized):**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

**What to Verify:**
✅ Status code is 401
✅ Access is denied without authentication

### Phase 2: User Management Testing

#### Test 5: Get Current User
**Endpoint:** GET `/api/users/me/`

**Headers:** Authorization: Bearer {{access_token}}

**Expected Response (200 OK):**
```json
{
    "user_id": "uuid",
    "username": "testuser1",
    "first_name": "Test",
    "last_name": "User",
    "email": "testuser1@example.com",
    "phone_number": "+1234567890",
    "role": "guest",
    "created_at": "2025-11-23T..."
}
```

**What to Verify:**
✅ Returns current authenticated user's data
✅ Password is not included in response

#### Test 6: Update User Profile
**Endpoint:** PATCH `/api/users/{{user_id}}/`

**Request Body:**
```json
{
    "first_name": "Updated",
    "phone_number": "+9876543210"
}
```

**Expected Response (200 OK):**
- Updated user data with new values

**What to Verify:**
✅ User can update their own profile
✅ Changes are reflected in response

### Phase 3: Conversation Management Testing

#### Test 7: Create Conversation
**Endpoint:** POST `/api/conversations/`

**Request Body:**
```json
{
    "participant_ids": ["{{user_id}}"]
}
```

**Expected Response (201 Created):**
```json
{
    "conversation_id": "uuid",
    "participants": [...],
    "messages": [],
    "message_count": 0,
    "created_at": "2025-11-23T..."
}
```

**What to Verify:**
✅ Conversation is created
✅ Creator is automatically added as participant
✅ conversation_id is saved to variables

#### Test 8: List Conversations
**Endpoint:** GET `/api/conversations/`

**Expected Response (200 OK):**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [...]
}
```

**What to Verify:**
✅ Returns only conversations where user is participant
✅ Pagination is applied
✅ Participants and messages are included

#### Test 9: Send Message to Conversation
**Endpoint:** POST `/api/conversations/{{conversation_id}}/add_message/`

**Request Body:**
```json
{
    "message_body": "Hello! This is a test message."
}
```

**Expected Response (201 Created):**
```json
{
    "message_id": "uuid",
    "sender": {...},
    "conversation": "uuid",
    "message_body": "Hello! This is a test message.",
    "sent_at": "2025-11-23T..."
}
```

**What to Verify:**
✅ Message is created successfully
✅ Sender is automatically set to current user
✅ Message is linked to conversation

#### Test 10: Get Conversation Messages (Pagination)
**Endpoint:** GET `/api/conversations/{{conversation_id}}/messages/?page=1`

**Expected Response (200 OK):**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [...]
}
```

**What to Verify:**
✅ Returns paginated messages (20 per page)
✅ Messages are ordered by sent_at descending
✅ Pagination info is included

### Phase 4: Message Management Testing

#### Test 11: List Messages with Pagination
**Endpoint:** GET `/api/messages/?page=1&page_size=20`

**Expected Response (200 OK):**
- Paginated list of messages from all conversations where user is participant

**What to Verify:**
✅ Returns 20 messages per page (default)
✅ Only messages from user's conversations are shown
✅ Pagination controls work correctly

#### Test 12: Filter Messages by Conversation
**Endpoint:** GET `/api/messages/?conversation_id={{conversation_id}}`

**What to Verify:**
✅ Returns only messages from specified conversation
✅ User must be participant to see messages

#### Test 13: Filter Messages by Time Range
**Endpoint:** GET `/api/messages/?sent_after=2025-11-01T00:00:00Z&sent_before=2025-11-30T23:59:59Z`

**What to Verify:**
✅ Returns only messages within specified time range
✅ Both sent_after and sent_before filters work
✅ Can use individual or combined filters

#### Test 14: Search Messages
**Endpoint:** GET `/api/messages/?search=test`

**What to Verify:**
✅ Returns messages containing search term
✅ Search is case-insensitive
✅ Searches in message_body field

#### Test 15: Update Own Message
**Endpoint:** PATCH `/api/messages/{{message_id}}/`

**Request Body:**
```json
{
    "message_body": "Updated message content"
}
```

**Expected Response (200 OK):**
- Updated message data

**What to Verify:**
✅ User can update their own messages
✅ Cannot update conversation or sender fields

#### Test 16: Delete Own Message
**Endpoint:** DELETE `/api/messages/{{message_id}}/`

**Expected Response (204 No Content)**

**What to Verify:**
✅ User can delete their own messages
✅ Message is removed from database

### Phase 5: Permission Testing

#### Test 17: Non-Participant Access Attempt
**Endpoint:** GET `/api/conversations/00000000-0000-0000-0000-000000000000/`

**Expected Response (403 Forbidden or 404 Not Found):**
```json
{
    "detail": "Not found." 
}
```

**What to Verify:**
✅ User cannot access conversations they're not part of
✅ Returns 403 or 404 (not in queryset)

#### Test 18: Update Another User's Message
**Setup:** Register a second user and create a message with that user

**Endpoint:** PATCH `/api/messages/{other-user-message-id}/`

**Expected Response (403 Forbidden):**
```json
{
    "detail": "You can only edit or delete your own messages."
}
```

**What to Verify:**
✅ User cannot update messages sent by others
✅ Returns 403 with appropriate error message

#### Test 19: Send Message to Non-Participant Conversation
**Setup:** Create conversation without current user

**Endpoint:** POST `/api/conversations/{other-conversation-id}/add_message/`

**Expected Response (403 Forbidden or 404 Not Found)**

**What to Verify:**
✅ User cannot send messages to conversations they're not part of
✅ Permission check prevents unauthorized message sending

### Phase 6: Additional Scenarios

#### Test 20: Register Multiple Users
Create 2-3 additional users to test:
- Multi-participant conversations
- Conversation filtering by participant
- Message access across different users

#### Test 21: Complex Filtering
**Endpoint:** GET `/api/messages/?conversation_id={{id}}&sent_after=2025-11-20T00:00:00Z&search=hello`

**What to Verify:**
✅ Multiple filters work together
✅ Results match all filter criteria

#### Test 22: Pagination Edge Cases
**Endpoint:** GET `/api/messages/?page=999`

**What to Verify:**
✅ Returns empty results for non-existent pages
✅ Pagination handles edge cases gracefully

## Expected Test Results Summary

### ✅ Authentication (5/5 tests should pass)
- User registration works
- Login returns valid JWT tokens
- Token refresh generates new tokens
- Unauthorized access is blocked
- Logout blacklists tokens

### ✅ Permissions (8/8 tests should pass)
- Only authenticated users can access API
- Only participants can view conversations
- Only participants can send messages
- Only message senders can edit/delete their messages
- Non-participants are denied access
- Proper error messages returned

### ✅ Pagination (4/4 tests should pass)
- Messages paginated at 20 per page
- Conversations paginated at 10 per page
- Pagination controls work correctly
- Can customize page size

### ✅ Filtering (5/5 tests should pass)
- Filter by conversation ID
- Filter by sender ID
- Filter by time range (sent_after, sent_before)
- Search in message body
- Multiple filters can be combined

## Troubleshooting

### Issue: 401 Unauthorized
**Solution:** Ensure access_token variable is set. Run login/register request first.

### Issue: 403 Forbidden
**Solution:** Verify user is a participant of the conversation being accessed.

### Issue: 404 Not Found
**Solution:** Check that the resource ID exists and is correct in variables.

### Issue: 500 Internal Server Error
**Solution:** Check Django server console for error details. Verify migrations are applied.

## API Security Checklist

✅ All endpoints require authentication (except register/login)
✅ JWT tokens used for stateless authentication
✅ Tokens have expiration (60 min for access, 1 day for refresh)
✅ Refresh token rotation enabled
✅ Token blacklisting on logout
✅ Passwords are hashed and never returned in responses
✅ Object-level permissions enforced
✅ Users can only access their own conversations
✅ Users can only edit/delete their own messages
✅ HTTPS should be used in production

## Next Steps

1. Run all tests in sequence using Postman Collection Runner
2. Verify all tests pass
3. Test edge cases and error scenarios
4. Document any issues or unexpected behavior
5. Submit project for manual QA review

## Support

For issues or questions:
- Check Django server logs
- Review DRF documentation: https://www.django-rest-framework.org/
- Review JWT documentation: https://django-rest-framework-simplejwt.readthedocs.io/

---
**Project:** ALX Backend Python - Messaging App
**Date:** November 23, 2025
**Version:** 1.0
