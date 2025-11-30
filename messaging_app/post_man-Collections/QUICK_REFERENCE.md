# Quick Reference - Messaging App API

## 🚀 Quick Start

```powershell
# Start server
cd "c:\Users\Admin\Downloads\New folder\alx-backend-python\messaging_app"
python manage.py runserver

# Server: http://127.0.0.1:8000
```

## 🔑 Authentication Flow

1. **Register:** `POST /api/auth/register/`
2. **Login:** `POST /api/auth/login/`
3. **Use Token:** Add header `Authorization: Bearer <access_token>`
4. **Refresh:** `POST /api/auth/token/refresh/` with refresh token
5. **Logout:** `POST /api/auth/logout/` with refresh token

## 📋 Common Requests

### Register User
```json
POST /api/auth/register/
{
    "username": "john",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe"
}
```

### Login
```json
POST /api/auth/login/
{
    "username": "john",
    "password": "SecurePass123!"
}
```

### Create Conversation
```json
POST /api/conversations/
Authorization: Bearer <token>
{
    "participant_ids": ["user-uuid"]
}
```

### Send Message
```json
POST /api/conversations/{id}/add_message/
Authorization: Bearer <token>
{
    "message_body": "Hello!"
}
```

### List Messages (Paginated)
```
GET /api/messages/?page=1&page_size=20
Authorization: Bearer <token>
```

### Filter Messages
```
GET /api/messages/?conversation_id=uuid&sent_after=2025-11-20T00:00:00Z&search=hello
Authorization: Bearer <token>
```

## 🔒 Permission Rules

| Endpoint | Who Can Access |
|----------|----------------|
| Register/Login | Anyone |
| List Users | Authenticated (own data) |
| List Conversations | Authenticated (participant only) |
| View Messages | Authenticated (participant only) |
| Send Message | Authenticated (participant only) |
| Edit Message | Authenticated (sender only) |
| Delete Message | Authenticated (sender only) |

## 📊 Pagination

- **Messages:** 20 per page (default)
- **Conversations:** 10 per page (default)
- **Custom:** Add `?page_size=50` (max 100 for messages)

## 🔍 Filtering Options

### Messages
- `?conversation_id=uuid` - By conversation
- `?sender_id=uuid` - By sender
- `?sent_after=2025-11-20T00:00:00Z` - After date
- `?sent_before=2025-11-25T23:59:59Z` - Before date
- `?search=hello` - Search text

### Conversations
- `?participant_id=uuid` - By participant ID
- `?participant_username=john` - By username
- `?created_after=2025-11-01T00:00:00Z` - After date
- `?created_before=2025-11-30T23:59:59Z` - Before date

## 🧪 Testing with Postman

1. **Import Collection:** `post_man-Collections/MessagingApp_API_Collection.json`
2. **Run Register:** Tokens auto-saved
3. **Test Endpoints:** Collection handles auth automatically
4. **22+ Tests:** Complete coverage included

## 📚 Documentation Files

- `TESTING_GUIDE.md` - Step-by-step testing instructions
- `PROJECT_DOCUMENTATION.md` - Complete technical documentation
- `IMPLEMENTATION_SUMMARY.md` - Implementation details
- `QUICK_REFERENCE.md` - This file

## ⚠️ Common Issues

**401 Unauthorized**
- Missing token → Login again
- Expired token → Use refresh endpoint

**403 Forbidden**
- Not a participant → Can't access conversation
- Not sender → Can't edit/delete message

**404 Not Found**
- Invalid UUID
- Resource doesn't exist
- Not in your conversations

## ✅ Status Codes

- `200` - Success
- `201` - Created
- `204` - Deleted
- `400` - Bad Request
- `401` - Unauthorized (no/invalid token)
- `403` - Forbidden (no permission)
- `404` - Not Found

## 🎯 Key Features

✅ JWT Authentication (60 min access, 1 day refresh)
✅ Token Rotation & Blacklisting
✅ Object-Level Permissions
✅ Pagination (20 messages/page)
✅ Advanced Filtering
✅ Search Functionality
✅ Secure Password Hashing
✅ Comprehensive Testing

## 📞 Need Help?

- Read `TESTING_GUIDE.md` for detailed instructions
- Check `PROJECT_DOCUMENTATION.md` for full docs
- Review Django server logs for errors
- Verify migrations: `python manage.py migrate`

---

**Ready to test! Import the Postman collection and start with the "Register User" request. 🚀**
