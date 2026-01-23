# Milestone 6: Deployment Submission Checklist

## Project Information
- **Student Name:** ___________________________
- **Project:** Django MessagingApp Deployment
- **Deployment Platform:** Render
- **Submission Date:** ___________________________

---

## Deployment URLs (Required for Submission)

Fill in your actual URLs:

```
Main Application URL: https://_____________________________.onrender.com

Swagger Documentation: https://_____________________________.onrender.com/swagger/

ReDoc Documentation: https://_____________________________.onrender.com/redoc/

Admin Panel: https://_____________________________.onrender.com/admin/

GitHub Repository: https://github.com/_____________________________
```

---

## Pre-Submission Checklist

### 1. Services Deployment ✓

- [ ] **PostgreSQL Database** created and available
  - Service name: _____________________________
  - Status: Available ⚪

- [ ] **Redis Instance** created and available
  - Service name: _____________________________
  - Status: Available ⚪

- [ ] **Web Service** deployed and live
  - Service name: _____________________________
  - Status: Live 🟢
  - No errors in logs

- [ ] **Celery Worker** deployed and running
  - Service name: _____________________________
  - Status: Running 🟢
  - Processing tasks successfully

---

### 2. Environment Configuration ✓

- [ ] All required environment variables set in Web Service
- [ ] All required environment variables set in Worker Service
- [ ] Database connection configured correctly
- [ ] Redis connection configured correctly
- [ ] Email configuration (Gmail) set up
- [ ] ALLOWED_HOSTS includes your Render domain
- [ ] SECRET_KEY is generated and secure
- [ ] DEBUG is set to False

**Environment Variables Checklist:**
- [ ] SECRET_KEY
- [ ] DEBUG
- [ ] ALLOWED_HOSTS
- [ ] DB_ENGINE, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
- [ ] CELERY_BROKER_URL, CELERY_RESULT_BACKEND
- [ ] EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
- [ ] CORS_ALLOW_ALL_ORIGINS, SECURE_SSL_REDIRECT

---

### 3. Swagger Documentation (Required) ✓

- [ ] Swagger UI accessible at `/swagger/`
- [ ] All API endpoints documented and visible
- [ ] Authentication section showing JWT Bearer token
- [ ] "Try it out" functionality working
- [ ] Schema includes:
  - [ ] User registration endpoint
  - [ ] User login endpoint
  - [ ] User management endpoints
  - [ ] Conversation endpoints (CRUD)
  - [ ] Message endpoints (CRUD)
  - [ ] Filtering and pagination documented

**Screenshot Required:**
- [ ] Take screenshot of Swagger UI showing all endpoints
- [ ] Save as `swagger_screenshot.png`

---

### 4. Application Testing ✓

#### A. User Authentication
- [ ] User registration successful
  ```bash
  Test user created: _____________________________
  ```
- [ ] User login returns JWT tokens
  ```bash
  Access token received: Yes ⚪ No ⚪
  ```
- [ ] Token refresh working
- [ ] Token verification working

#### B. API Endpoints
- [ ] GET `/api/users/` - List users (authenticated)
- [ ] GET `/api/users/me/` - Current user profile
- [ ] POST `/api/conversations/` - Create conversation
- [ ] GET `/api/conversations/` - List conversations
- [ ] POST `/api/messages/` - Send message
- [ ] GET `/api/messages/` - List messages
- [ ] Filtering working (e.g., by conversation_id)
- [ ] Pagination working (20 items per page)

#### C. Background Tasks (Celery)
- [ ] Celery worker logs showing activity
- [ ] Email notification triggered when message sent
- [ ] Email successfully received
  ```bash
  Test email sent to: _____________________________
  Email received: Yes ⚪ No ⚪
  ```

#### D. Database Operations
- [ ] Database migrations completed successfully
- [ ] Data persists after service restart
- [ ] No database connection errors

---

### 5. Security Checks ✓

- [ ] HTTPS enabled (automatic on Render)
- [ ] SSL certificate valid
- [ ] No sensitive data in logs
- [ ] No secrets exposed in GitHub repository
- [ ] `.env` file in `.gitignore`
- [ ] CORS configured correctly (not allowing all origins)
- [ ] Security middleware active
- [ ] CSRF protection enabled

---

### 6. Code Quality ✓

- [ ] All code pushed to GitHub
- [ ] Latest commit message is meaningful
- [ ] No syntax errors
- [ ] No critical warnings
- [ ] All required files present:
  - [ ] `render.yaml`
  - [ ] `build.sh`
  - [ ] `Procfile`
  - [ ] `requirements.txt`
  - [ ] `runtime.txt`
  - [ ] `README.md`
  - [ ] Documentation files

---

### 7. Documentation ✓

- [ ] README.md updated with deployment info
- [ ] API endpoints documented
- [ ] Setup instructions clear
- [ ] Environment variables documented
- [ ] Deployment guide included
- [ ] Screenshots included (if required)

---

## Functional Testing Log

### Test 1: User Registration
```bash
Endpoint: POST /api/auth/register/
Status Code: _____
Response: _________________________________
Result: Pass ⚪ Fail ⚪
```

### Test 2: User Login
```bash
Endpoint: POST /api/auth/login/
Status Code: _____
Access Token Received: Yes ⚪ No ⚪
Result: Pass ⚪ Fail ⚪
```

### Test 3: Create Conversation
```bash
Endpoint: POST /api/conversations/
Status Code: _____
Conversation ID: _____
Result: Pass ⚪ Fail ⚪
```

### Test 4: Send Message
```bash
Endpoint: POST /api/messages/
Status Code: _____
Message ID: _____
Result: Pass ⚪ Fail ⚪
```

### Test 5: Email Notification
```bash
Email Sent to Celery: Yes ⚪ No ⚪
Email Received: Yes ⚪ No ⚪
Result: Pass ⚪ Fail ⚪
```

### Test 6: Swagger Access
```bash
URL: /swagger/
Accessible: Yes ⚪ No ⚪
All Endpoints Visible: Yes ⚪ No ⚪
Result: Pass ⚪ Fail ⚪
```

---

## Performance Checks

- [ ] First request response time: _____ seconds (cold start)
- [ ] Subsequent request response time: _____ seconds
- [ ] Database query time: _____ ms
- [ ] Celery task processing time: _____ seconds
- [ ] No memory issues in logs
- [ ] No timeout errors

---

## Logs Verification

### Web Service Logs
```
Last 10 lines checked: _____________________________
Errors found: Yes ⚪ No ⚪
If yes, describe: _____________________________
```

### Worker Service Logs
```
Celery worker status: Running ⚪ Stopped ⚪
Tasks processed: _____
Errors found: Yes ⚪ No ⚪
```

### Database Logs
```
Connection status: Connected ⚪ Error ⚪
Migrations applied: _____
```

---

## Known Issues (if any)

List any known issues or limitations:

1. _____________________________
2. _____________________________
3. _____________________________

---

## Additional Notes

_________________________________________________________________________
_________________________________________________________________________
_________________________________________________________________________

---

## Final Verification

Before submitting, I confirm that:

- [ ] Application is fully deployed and accessible
- [ ] Swagger documentation is public at `/swagger/`
- [ ] Celery workers are running and processing tasks
- [ ] Email notifications are working
- [ ] All tests pass successfully
- [ ] No critical errors in logs
- [ ] GitHub repository is up to date
- [ ] All documentation is complete

---

## Submission Information

**Submit the following:**

1. **URLs Document** (this checklist with all URLs filled)
2. **GitHub Repository Link**
3. **Screenshots:**
   - Swagger UI showing all endpoints
   - Render dashboard showing all services "Live/Running"
   - Email notification received
   - Sample API response
4. **Optional:** Video demo (if required)

---

## Submission Date and Time

- **Date:** _____________________________
- **Time:** _____________________________
- **Submitted By:** _____________________________

---

## Reviewer Notes (for QA reviewer)

_________________________________________________________________________
_________________________________________________________________________
_________________________________________________________________________

**Score:** _____ / 100

**Reviewer:** _____________________________
**Date:** _____________________________

---

## Resources Used

- [RENDER_DEPLOYMENT_GUIDE.md](RENDER_DEPLOYMENT_GUIDE.md) - Full deployment guide
- [QUICK_DEPLOY.md](QUICK_DEPLOY.md) - Quick reference
- [ENV_VARIABLES_GUIDE.md](ENV_VARIABLES_GUIDE.md) - Environment variables
- [Render Documentation](https://render.com/docs/deploy-django)

---

**Good luck with your submission! 🚀**

Remember: 
- Test everything before submitting
- Double-check all URLs are accessible
- Ensure Swagger documentation is public
- Verify Celery is working with actual email test

**Deadline:** January 25, 2026 11:59 PM
