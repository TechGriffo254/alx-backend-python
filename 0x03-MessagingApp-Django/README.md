# Django MessagingApp - Full-Stack Messaging Application

A comprehensive Django REST API messaging application with real-time notifications, JWT authentication, and background task processing using Celery.

## 🚀 Live Demo

- **Application:** https://your-app.onrender.com
- **API Documentation (Swagger):** https://your-app.onrender.com/swagger/
- **ReDoc Documentation:** https://your-app.onrender.com/redoc/

## 📋 Features

### Core Features
- ✅ User authentication (JWT-based)
- ✅ User registration and profile management
- ✅ Conversation management (create, read, update, delete)
- ✅ Message management (send, receive, edit, delete)
- ✅ Real-time email notifications
- ✅ Background task processing with Celery
- ✅ Advanced filtering and search
- ✅ Pagination (20 items per page)
- ✅ Role-based permissions
- ✅ API documentation (Swagger & ReDoc)

### Security Features
- 🔒 JWT authentication with token refresh
- 🔒 Password hashing and validation
- 🔒 HTTPS/SSL encryption
- 🔒 CORS configuration
- 🔒 CSRF protection
- 🔒 Rate limiting
- 🔒 Secure headers

### Additional Features
- 📧 Email notifications via Celery
- 📊 Request logging middleware
- ⏰ Time-based access control
- 🚫 Offensive language filtering
- 👥 Role-based permission middleware

## 🛠️ Technology Stack

- **Backend Framework:** Django 5.2.7
- **API Framework:** Django REST Framework 3.15.2
- **Authentication:** JWT (djangorestframework-simplejwt)
- **Task Queue:** Celery 5.4.0
- **Message Broker:** Redis/RabbitMQ
- **Database:** PostgreSQL (Production) / SQLite (Development)
- **Documentation:** drf-yasg (Swagger/OpenAPI)
- **Server:** Gunicorn
- **Static Files:** WhiteNoise
- **Deployment:** Render

## 📁 Project Structure

```
0x03-MessagingApp-Django/
├── chats/                          # Main app directory
│   ├── models.py                   # User, Conversation, Message models
│   ├── serializers.py              # DRF serializers
│   ├── views.py                    # API viewsets
│   ├── urls.py                     # App-level URL routing
│   ├── permissions.py              # Custom permissions
│   ├── filters.py                  # Django-filter configurations
│   ├── pagination.py               # Custom pagination
│   ├── tasks.py                    # Celery tasks
│   ├── middleware.py               # Custom middleware
│   ├── auth.py                     # Authentication views
│   └── migrations/                 # Database migrations
├── messaging_app/                  # Project directory
│   ├── settings.py                 # Django settings
│   ├── urls.py                     # Root URL routing
│   ├── wsgi.py                     # WSGI config
│   ├── asgi.py                     # ASGI config
│   └── celery.py                   # Celery configuration
├── post_man-Collections/           # API documentation
│   ├── MessagingApp_API_Collection.json
│   ├── TESTING_GUIDE.md
│   └── IMPLEMENTATION_SUMMARY.md
├── build.sh                        # Build script for deployment
├── Procfile                        # Process file for services
├── render.yaml                     # Render deployment config
├── requirements.txt                # Python dependencies
├── runtime.txt                     # Python version
├── manage.py                       # Django management script
├── RENDER_DEPLOYMENT_GUIDE.md      # Full deployment guide
├── QUICK_DEPLOY.md                 # Quick deployment reference
├── ENV_VARIABLES_GUIDE.md          # Environment variables guide
└── SUBMISSION_CHECKLIST_M6.md      # Project submission checklist
```

## 🚦 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL (for production)
- Redis (for Celery)
- Git

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/yourrepo.git
   cd 0x03-MessagingApp-Django
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server:**
   ```bash
   python manage.py runserver
   ```

8. **Run Celery worker (in another terminal):**
   ```bash
   celery -A messaging_app worker --loglevel=info
   ```

9. **Access the application:**
   - API: http://localhost:8000
   - Swagger: http://localhost:8000/swagger/
   - Admin: http://localhost:8000/admin/

## 🌐 Deployment to Render

### Option 1: Quick Deploy (Recommended)

See [QUICK_DEPLOY.md](QUICK_DEPLOY.md) for fast deployment steps.

### Option 2: Detailed Deployment

See [RENDER_DEPLOYMENT_GUIDE.md](RENDER_DEPLOYMENT_GUIDE.md) for comprehensive instructions.

### Deployment Summary

1. Push code to GitHub
2. Create Render account
3. Create services:
   - PostgreSQL database
   - Redis instance
   - Web service (Django)
   - Background worker (Celery)
4. Configure environment variables
5. Deploy and test

## 📖 API Documentation

### Authentication Endpoints

```http
POST /api/auth/register/        # Register new user
POST /api/auth/login/           # Login and get JWT tokens
POST /api/auth/logout/          # Logout (blacklist token)
POST /api/auth/token/           # Obtain JWT token
POST /api/auth/token/refresh/   # Refresh JWT token
POST /api/auth/token/verify/    # Verify JWT token
```

### User Endpoints

```http
GET    /api/users/              # List all users
POST   /api/users/              # Create user
GET    /api/users/{id}/         # Get user details
PUT    /api/users/{id}/         # Update user
DELETE /api/users/{id}/         # Delete user
GET    /api/users/me/           # Get current user
```

### Conversation Endpoints

```http
GET    /api/conversations/               # List conversations
POST   /api/conversations/               # Create conversation
GET    /api/conversations/{id}/          # Get conversation
PUT    /api/conversations/{id}/          # Update conversation
DELETE /api/conversations/{id}/          # Delete conversation
GET    /api/conversations/{id}/messages/ # Get conversation messages
```

### Message Endpoints

```http
GET    /api/messages/           # List messages
POST   /api/messages/           # Send message (triggers email)
GET    /api/messages/{id}/      # Get message details
PUT    /api/messages/{id}/      # Update message
DELETE /api/messages/{id}/      # Delete message
```

### Filtering & Search

```http
# Filter messages by conversation
GET /api/messages/?conversation_id=1

# Search users by name
GET /api/users/?search=john

# Pagination
GET /api/messages/?page=2

# Ordering
GET /api/messages/?ordering=-created_at
```

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### Getting a Token

```bash
curl -X POST https://your-app.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Using the Token

Include the access token in the Authorization header:

```bash
curl -X GET https://your-app.onrender.com/api/users/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

## 🧪 Testing

### Run Tests

```bash
python manage.py test
```

### Test Coverage

```bash
coverage run --source='.' manage.py test
coverage report
```

### API Testing with Postman

Import the Postman collection from `post_man-Collections/MessagingApp_API_Collection.json`

## 📧 Email Notifications

The application sends email notifications asynchronously using Celery when:
- A new message is sent
- A user is added to a conversation

### Configuration

Set up email in environment variables:
```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 🔧 Configuration

### Environment Variables

See [ENV_VARIABLES_GUIDE.md](ENV_VARIABLES_GUIDE.md) for complete configuration details.

Key variables:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (False in production)
- `ALLOWED_HOSTS`: Allowed domain names
- `DB_*`: Database configuration
- `CELERY_*`: Celery configuration
- `EMAIL_*`: Email configuration

## 📊 Database Schema

### User Model
- Extended Django User model
- Fields: username, email, password, first_name, last_name, phone_number, role

### Conversation Model
- Fields: participants (M2M with User), created_at

### Message Model
- Fields: conversation (FK), sender (FK), message_body, sent_at

## 🎯 Middleware

Custom middleware included:
1. **RequestLoggingMiddleware**: Logs all requests
2. **RestrictAccessByTimeMiddleware**: Time-based access control (9 AM - 6 PM)
3. **OffensiveLanguageMiddleware**: Filters offensive content
4. **RolePermissionMiddleware**: Enforces role-based permissions

## 🐛 Troubleshooting

### Common Issues

1. **Cold Start Delay (Render Free Tier)**
   - First request may take 30-60 seconds
   - Solution: Normal behavior, subsequent requests are fast

2. **Email Not Sending**
   - Check Celery worker is running
   - Verify email credentials
   - Check Gmail app password (not regular password)

3. **Database Connection Error**
   - Verify DB environment variables
   - Use internal database URL on Render

4. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check WhiteNoise configuration

See [RENDER_DEPLOYMENT_GUIDE.md](RENDER_DEPLOYMENT_GUIDE.md) for more troubleshooting.

## 📝 License

This project is licensed under the MIT License.

## 👥 Contributors

- Your Name - Initial work

## 🙏 Acknowledgments

- ALX Backend Python Program
- Django Documentation
- Django REST Framework
- Celery Documentation
- Render Documentation

## 📞 Support

For issues and questions:
- Create an issue in the GitHub repository
- Check documentation files
- Review Render logs

## 🗓️ Project Timeline

- **Start Date:** January 12, 2026
- **Deadline:** January 25, 2026 11:59 PM
- **Milestone:** 6 - Deployment and Documentation

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [Render Documentation](https://render.com/docs)
- [drf-yasg Documentation](https://drf-yasg.readthedocs.io/)

---

**Status:** ✅ Ready for Deployment

**Last Updated:** January 23, 2026
