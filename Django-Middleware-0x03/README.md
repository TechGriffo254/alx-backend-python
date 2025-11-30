# Django Middleware Project - 0x03

Comprehensive implementation of custom Django middleware for request logging, time-based access control, rate limiting, and role-based permissions.

## 🚀 Quick Start

```powershell
cd Django-Middleware-0x03
python manage.py runserver
```

## 📋 Implemented Middleware

### 1. RequestLoggingMiddleware ✅
Logs all requests to `requests.log` with timestamp, user, and path.

### 2. RestrictAccessByTimeMiddleware ✅
Restricts access to 9:00 AM - 6:00 PM only. Returns 403 outside these hours.

### 3. OffensiveLanguageMiddleware ✅  
Rate limiting: Maximum 5 POST requests per minute per IP address.

### 4. RolePermissionMiddleware ✅
Restricts API access to admin and moderator roles only.

## 📝 Testing

See full documentation in project files for detailed testing instructions.

---

**Status:** ✅ Complete | **Date:** November 23, 2025
