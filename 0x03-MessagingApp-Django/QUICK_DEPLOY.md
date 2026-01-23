# Quick Deployment Reference - Render

## TL;DR - Fast Deployment Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2. Create Render Account
- Go to https://render.com
- Sign up with GitHub

### 3. Create Services (Manual Method)

#### A. PostgreSQL Database
```
New + → PostgreSQL
Name: messaging-app-db
Plan: Free
Create Database
```
**Save the Internal Database URL**

#### B. Redis
```
New + → Redis
Name: messaging-app-redis
Plan: Free
Create Redis
```
**Save the Internal Redis URL**

#### C. Web Service
```
New + → Web Service
Connect GitHub repository
Name: messaging-app-web
Runtime: Python 3
Build Command: ./build.sh
Start Command: gunicorn messaging_app.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120
Plan: Free
```

#### D. Background Worker (Celery)
```
New + → Background Worker
Connect GitHub repository
Name: messaging-app-celery-worker
Build Command: pip install -r requirements.txt
Start Command: celery -A messaging_app worker --loglevel=info
Plan: Free
```

---

## Essential Environment Variables

Copy these to **both Web Service and Worker**:

### Database (from PostgreSQL service)
```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<from_postgres_service>
DB_USER=<from_postgres_service>
DB_PASSWORD=<from_postgres_service>
DB_HOST=<internal_host_from_postgres>
DB_PORT=5432
```

### Django
```bash
SECRET_KEY=<auto_generated>
DEBUG=False
ALLOWED_HOSTS=<your-app>.onrender.com
```

### Celery (from Redis service)
```bash
CELERY_BROKER_URL=<redis_internal_url>
CELERY_RESULT_BACKEND=<redis_internal_url>
```

### Email (Gmail)
```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=<gmail_app_password>
DEFAULT_FROM_EMAIL=noreply@messagingapp.com
```

### Security
```bash
CORS_ALLOW_ALL_ORIGINS=False
SECURE_SSL_REDIRECT=True
```

---

## Gmail App Password Setup

1. Google Account → Security → 2-Step Verification (enable)
2. Security → App passwords
3. Generate password for "Mail"
4. Copy 16-character password
5. Use as `EMAIL_HOST_PASSWORD`

---

## Testing URLs

Replace `<your-app>` with your Render app name:

- **App:** https://`<your-app>`.onrender.com
- **Swagger:** https://`<your-app>`.onrender.com/swagger/
- **ReDoc:** https://`<your-app>`.onrender.com/redoc/
- **Admin:** https://`<your-app>`.onrender.com/admin/

---

## Quick Tests

### 1. Test Swagger
```bash
curl https://<your-app>.onrender.com/swagger/
```

### 2. Test Registration
```bash
curl -X POST https://<your-app>.onrender.com/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123!",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### 3. Test Login
```bash
curl -X POST https://<your-app>.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPass123!"
  }'
```

---

## Common Issues & Quick Fixes

### Build Fails
```bash
# Make build.sh executable locally first
chmod +x build.sh
git add build.sh
git commit -m "Make build.sh executable"
git push
```

### Database Connection Error
- Verify DB environment variables match PostgreSQL service
- Use **Internal Database URL**, not External

### Celery Not Working
- Check Redis URL is the **Internal URL**
- Verify worker service is "Running" in dashboard

### Static Files Not Loading
- Check logs: "Collecting static files"
- Verify `whitenoise` in `MIDDLEWARE`

### Swagger 404
- Check `/swagger/` in `urls.py`
- Verify `drf_yasg` in `INSTALLED_APPS`

---

## Submission URLs Format

For your assignment submission:

```
Application URL: https://messaging-app-web-xxxx.onrender.com
Swagger Documentation: https://messaging-app-web-xxxx.onrender.com/swagger/
GitHub Repository: https://github.com/yourusername/yourrepo
```

---

## Pre-Submission Checklist

- [ ] All services showing "Live" or "Running"
- [ ] Swagger accessible and showing all endpoints
- [ ] User registration working
- [ ] Login returning JWT tokens
- [ ] Email notifications being sent
- [ ] No errors in service logs
- [ ] Database migrations completed

---

## Monitoring

### Check Service Health
```
Render Dashboard → Your Service → Logs
```

### Common Log Messages (Good Signs)
```
✓ Collecting static files... done
✓ Running migrations... done
✓ Gunicorn is running
✓ Celery worker is ready
✓ Connected to database
```

---

## Need Help?

1. Check [RENDER_DEPLOYMENT_GUIDE.md](RENDER_DEPLOYMENT_GUIDE.md) for detailed instructions
2. Review Render service logs
3. Check [Render Docs](https://render.com/docs/deploy-django)

---

**Remember:** First request after inactivity takes 30-60 seconds (cold start). This is normal for free tier!

Good luck! 🚀
