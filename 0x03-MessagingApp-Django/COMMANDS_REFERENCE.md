# Quick Command Reference

## 🚀 Deployment Commands

### Push to GitHub
```bash
# Check current status
git status

# Add all changes
git add .

# Commit with message
git commit -m "Ready for Render deployment"

# Push to remote
git push origin main

# Verify push
git log --oneline -5
```

---

## 🧪 Local Testing Commands

### Django Management
```bash
# Run development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Check for issues
python manage.py check

# Check deployment readiness
python manage.py check --deploy

# Open Django shell
python manage.py shell

# Run tests
python manage.py test
```

### Celery Commands
```bash
# Start Celery worker
celery -A messaging_app worker --loglevel=info

# Start Celery beat (scheduler)
celery -A messaging_app beat --loglevel=info

# Start worker with beat
celery -A messaging_app worker --beat --loglevel=info

# Monitor Celery tasks
celery -A messaging_app inspect active

# Stop all workers
celery -A messaging_app control shutdown
```

### Database Commands
```bash
# Create database backup
python manage.py dumpdata > backup.json

# Load database backup
python manage.py loaddata backup.json

# Show migrations
python manage.py showmigrations

# SQL for migration
python manage.py sqlmigrate chats 0001

# Reset database (SQLite only - development)
rm db.sqlite3
python manage.py migrate
```

---

## 🌐 API Testing Commands

### User Registration
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123!",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### User Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPass123!"
  }'
```

### Get Token
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPass123!"
  }'
```

### List Users (Authenticated)
```bash
curl -X GET http://localhost:8000/api/users/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Create Conversation
```bash
curl -X POST http://localhost:8000/api/conversations/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "participant_ids": [1, 2]
  }'
```

### Send Message
```bash
curl -X POST http://localhost:8000/api/messages/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": 1,
    "message_body": "Hello, World!"
  }'
```

### List Messages
```bash
curl -X GET http://localhost:8000/api/messages/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Filter Messages by Conversation
```bash
curl -X GET "http://localhost:8000/api/messages/?conversation_id=1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🐳 Production Testing (Render)

Replace `your-app` with your Render app name:

### Check Application Health
```bash
curl https://your-app.onrender.com/
```

### Check Swagger
```bash
curl https://your-app.onrender.com/swagger/
```

### Production Registration
```bash
curl -X POST https://your-app.onrender.com/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "produser",
    "email": "prod@example.com",
    "password": "ProdPass123!",
    "first_name": "Prod",
    "last_name": "User"
  }'
```

### Production Login
```bash
curl -X POST https://your-app.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "produser",
    "password": "ProdPass123!"
  }'
```

---

## 🔧 Virtual Environment Commands

### Create Virtual Environment
```bash
# Windows
python -m venv venv

# Linux/Mac
python3 -m venv venv
```

### Activate Virtual Environment
```bash
# Windows PowerShell
venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

### Deactivate Virtual Environment
```bash
deactivate
```

### Install Requirements
```bash
pip install -r requirements.txt
```

### Update Requirements
```bash
pip freeze > requirements.txt
```

---

## 📦 Package Management

### Install Package
```bash
pip install package-name
```

### Install Specific Version
```bash
pip install package-name==1.2.3
```

### Uninstall Package
```bash
pip uninstall package-name
```

### List Installed Packages
```bash
pip list
```

### Show Package Info
```bash
pip show package-name
```

### Check for Updates
```bash
pip list --outdated
```

---

## 🔍 Debugging Commands

### Check Python Version
```bash
python --version
```

### Check Django Version
```bash
python -m django --version
```

### Check Installed Packages
```bash
pip show django
pip show celery
pip show gunicorn
```

### Test Database Connection
```bash
python manage.py dbshell
```

### View Current Settings
```bash
python manage.py diffsettings
```

### Validate Models
```bash
python manage.py validate
```

---

## 📊 Monitoring Commands

### View Logs (Local)
```bash
# Django logs
tail -f app.log

# Celery logs (if logging to file)
tail -f celery.log
```

### Check Process Status
```bash
# Windows
tasklist | findstr python

# Linux/Mac
ps aux | grep python
ps aux | grep celery
```

### Kill Process
```bash
# Windows (find PID first with tasklist)
taskkill /PID <pid> /F

# Linux/Mac
kill <pid>
killall celery
```

---

## 🔑 Environment Variables (Local)

### Set Environment Variable (Windows PowerShell)
```powershell
$env:DEBUG="True"
$env:SECRET_KEY="your-secret-key"
```

### Set Environment Variable (Windows CMD)
```cmd
set DEBUG=True
set SECRET_KEY=your-secret-key
```

### Set Environment Variable (Linux/Mac)
```bash
export DEBUG=True
export SECRET_KEY=your-secret-key
```

### Load from .env File
```bash
# Ensure python-decouple is installed
pip install python-decouple

# Create .env file
cp .env.example .env

# Edit .env with your values
nano .env  # or use any text editor
```

---

## 🧹 Cleanup Commands

### Remove Compiled Python Files
```bash
# Windows
Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item
Get-ChildItem -Recurse -Filter "__pycache__" | Remove-Item -Recurse

# Linux/Mac
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -delete
```

### Remove Migration Files (careful!)
```bash
# Windows
Get-ChildItem -Path "chats\migrations" -Filter "*.py" | Where-Object { $_.Name -ne "__init__.py" } | Remove-Item

# Linux/Mac
find chats/migrations -name "*.py" ! -name "__init__.py" -delete
```

### Clear Static Files
```bash
rm -rf staticfiles/
python manage.py collectstatic --noinput
```

---

## 🎯 Pre-Deployment Checks

### Run All Checks
```bash
# Check for issues
python manage.py check

# Check deployment readiness
python manage.py check --deploy --fail-level=WARNING

# Check migrations
python manage.py showmigrations

# Check static files
python manage.py collectstatic --dry-run --noinput

# Run tests
python manage.py test

# Verify requirements
pip check
```

---

## 📝 Git Commands Reference

### Repository Status
```bash
git status
git log --oneline -10
git branch
git remote -v
```

### Branching
```bash
git branch feature-name
git checkout feature-name
git checkout -b feature-name  # create and checkout
git merge feature-name
git branch -d feature-name  # delete branch
```

### Stashing Changes
```bash
git stash
git stash list
git stash pop
git stash apply
git stash drop
```

### Undo Changes
```bash
git checkout -- filename  # discard changes to file
git reset HEAD filename   # unstage file
git reset --hard HEAD     # discard all changes (careful!)
```

### View Changes
```bash
git diff
git diff --staged
git show commit-hash
```

---

## 🚨 Emergency Commands

### Reset to Last Commit (careful!)
```bash
git reset --hard HEAD
```

### Force Push (very careful!)
```bash
git push --force origin main
```

### Remove File from Git (keep locally)
```bash
git rm --cached filename
```

### Fix Committed .env File
```bash
git rm --cached .env
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Remove .env from tracking"
```

---

## 💡 Quick Tips

### Create Superuser Quickly
```bash
python manage.py createsuperuser --noinput --username admin --email admin@example.com
```

### Run Server on Different Port
```bash
python manage.py runserver 8080
```

### Run Server on All Interfaces
```bash
python manage.py runserver 0.0.0.0:8000
```

### Execute Python Code
```bash
python manage.py shell -c "from chats.models import User; print(User.objects.count())"
```

### One-Line Celery Test
```bash
python -c "from chats.tasks import send_email_notification; send_email_notification.delay('test@example.com', 'Test', 'Test message')"
```

---

## 📱 VS Code Terminal Shortcuts

```bash
# Open new terminal
Ctrl + Shift + `

# Split terminal
Ctrl + Shift + 5

# Kill terminal
Ctrl + C (in terminal)

# Clear terminal
Ctrl + L or type 'clear'
```

---

## 🔗 Useful URLs (Local Development)

```
Application: http://localhost:8000/
Admin: http://localhost:8000/admin/
Swagger: http://localhost:8000/swagger/
ReDoc: http://localhost:8000/redoc/
API Root: http://localhost:8000/api/
```

---

## 🔗 Useful URLs (Production - Replace 'your-app')

```
Application: https://your-app.onrender.com/
Admin: https://your-app.onrender.com/admin/
Swagger: https://your-app.onrender.com/swagger/
ReDoc: https://your-app.onrender.com/redoc/
API Root: https://your-app.onrender.com/api/
```

---

**Quick Access:** Bookmark this file for easy command reference during development and deployment!
