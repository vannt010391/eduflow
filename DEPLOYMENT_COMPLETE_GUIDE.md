# Eduflow Complete Deployment Guide

## Overview
This guide covers 3 deployment options for Eduflow:
1. **Traditional Ubuntu 24.04** with Nginx, Gunicorn, and SQLite
2. **Docker** with Docker Compose (PostgreSQL + Redis included)
3. **GitHub Actions CI/CD** for automated deployment

## Quick Start

### Option 1: Traditional Ubuntu 24.04 Deployment

#### Prerequisites
- Ubuntu 24.04 LTS server with SSH access
- 2+ GB RAM recommended
- Domain name (optional but recommended for SSL)

#### Deployment Steps

```bash
# SSH into your server
ssh user@your-server-ip

# Download and run the deployment script
wget https://raw.githubusercontent.com/vannt010391/eduflow/feature/update-function/deploy.sh
sudo bash deploy.sh yourdomain.com admin@yourdomain.com

# That's it! The script will handle everything
```

The deployment script will:
- ✅ Update system packages
- ✅ Install Python 3, Nginx, Git, Certbot
- ✅ Clone the project from GitHub
- ✅ Set up Python virtual environment
- ✅ Install dependencies
- ✅ Configure Django settings
- ✅ Run migrations
- ✅ Set up Gunicorn service
- ✅ Configure Nginx reverse proxy
- ✅ Install SSL certificate (Let's Encrypt)
- ✅ Configure firewall
- ✅ Set up automated backups
- ✅ Enable Fail2Ban security

#### Manual Steps (if not using script)

```bash
# 1. SSH to server and update
sudo apt update && sudo apt upgrade -y

# 2. Install dependencies
sudo apt install -y python3 python3-pip python3-venv git nginx curl

# 3. Clone project
cd /opt
sudo git clone --branch feature/update-function https://github.com/vannt010391/eduflow.git

# 4. Create virtual environment
cd /opt/eduflow
python3 -m venv venv
source venv/bin/activate

# 5. Install Python packages
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# 6. Configure .env
cp .env.example .env
nano .env  # Edit with your settings

# 7. Run migrations and collect static files
python manage.py migrate
python manage.py collectstatic --noinput

# 8. Create superuser
python manage.py createsuperuser

# 9. Configure Gunicorn service (see DEPLOYMENT_UBUNTU_24.04.md)

# 10. Configure Nginx (see DEPLOYMENT_UBUNTU_24.04.md)

# 11. Set up SSL with Let's Encrypt
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

### Option 2: Docker Deployment

#### Prerequisites
- Docker and Docker Compose installed
- Port 80 and 443 available
- Domain name (recommended)

#### Quick Start with Docker

```bash
# 1. Clone the project
git clone --branch feature/update-function https://github.com/vannt010391/eduflow.git
cd eduflow

# 2. Create .env file
cp .env.example .env
nano .env  # Update with your settings

# 3. Create SSL certificates directory (optional but recommended)
mkdir -p ssl
# Place your cert.pem and key.pem in ssl/ directory, or use self-signed:
openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes

# 4. Start the application
docker-compose up -d

# 5. Create superuser
docker-compose exec web python manage.py createsuperuser

# 6. Verify
docker-compose ps
curl http://localhost
```

#### Docker Services

The `docker-compose.yml` includes:
- **Web**: Django/Gunicorn application on port 8000
- **Nginx**: Reverse proxy on ports 80 and 443
- **PostgreSQL**: Database server (optional, SQLite is default)
- **Redis**: Caching and session storage

#### Common Docker Commands

```bash
# View logs
docker-compose logs -f web

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Run Django commands
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# Backup database
docker-compose exec db pg_dump -U eduflow_user eduflow > backup.sql

# Shell access
docker-compose exec web /bin/bash
```

#### Update Docker Images

```bash
# Pull latest code
git pull origin feature/update-function

# Rebuild images
docker-compose build

# Restart with new images
docker-compose up -d
```

---

### Option 3: GitHub Actions CI/CD Pipeline

#### Setup

1. **Configure GitHub Repository Secrets**

Go to Settings → Secrets and variables → Actions, and add:

```
HOST              - Your server IP address
USERNAME          - SSH username (e.g., ubuntu)
SSH_KEY           - Your SSH private key (multiline)
PORT              - SSH port (usually 22)
DOCKER_USERNAME   - Docker Hub username (optional)
DOCKER_PASSWORD   - Docker Hub access token (optional)
SLACK_WEBHOOK     - Slack webhook URL (optional)
USE_DOCKER        - Set to 'true' to use Docker deployment
```

2. **Generate SSH Key for GitHub Actions**

```bash
# On your local machine
ssh-keygen -t ed25519 -f github_actions_key -C "github-actions"

# Copy public key to server
ssh-copy-id -i github_actions_key.pub user@your-server-ip

# Add private key to GitHub secrets
cat github_actions_key | pbcopy  # macOS
# or
cat github_actions_key  # Copy the output and paste in GitHub Secrets
```

3. **Workflows Included**

**tests.yml** - Runs on every push/PR
- Tests with Python 3.9, 3.10, 3.11
- Database migrations
- Code coverage
- Security scanning with Trivy
- Code quality checks (Black, isort, pylint)

**deploy.yml** - Runs on main branch push
- Tests first
- Deploys to production server
- Docker deployment option
- Slack notifications

#### Triggering Deployment

Just push to main branch:
```bash
git checkout main
git merge feature/update-function
git push origin main
```

The GitHub Actions pipeline will:
1. Run tests
2. Deploy to production
3. Send Slack notification on success/failure

---

## Configuration Guide

### Django Settings

#### For Traditional Deployment
Edit `eduflow_ai/settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

#### For Production (PostgreSQL)
In `.env`:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=eduflow
DB_USER=eduflow_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432
```

### Database

#### SQLite (Default)
- Simple, no additional setup needed
- Good for small deployments
- Daily backups recommended

#### PostgreSQL (Recommended for Production)
- Better performance
- Concurrent user handling
- Automated backups in Docker

### Email Configuration

In `.env`:
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
```

### Claude AI Configuration

```
AI_ENABLED=True
AI_PROVIDER=anthropic
AI_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxx
AI_MODEL=claude-3-5-sonnet-20241022
```

---

## Monitoring and Maintenance

### View Logs

**Traditional Deployment:**
```bash
# Django/Gunicorn
sudo journalctl -u eduflow.service -f

# Nginx
sudo tail -f /var/log/nginx/error.log
```

**Docker:**
```bash
docker-compose logs -f web
docker-compose logs -f nginx
```

### Backups

**Traditional:**
```bash
# Manual backup
cp /opt/eduflow/db.sqlite3 /backups/eduflow/backup_$(date +%Y%m%d).sqlite3

# Restore
cp /backups/eduflow/backup_YYYYMMDD.sqlite3 /opt/eduflow/db.sqlite3
sudo systemctl restart eduflow.service
```

**Docker:**
```bash
# PostgreSQL backup
docker-compose exec db pg_dump -U eduflow_user eduflow > backup.sql

# Restore
cat backup.sql | docker-compose exec -T db psql -U eduflow_user eduflow
```

### Update Application

**Traditional:**
```bash
cd /opt/eduflow
source venv/bin/activate
git pull origin feature/update-function
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart eduflow.service
```

**Docker:**
```bash
git pull origin feature/update-function
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py migrate
```

### Performance Monitoring

```bash
# Check disk space
df -h

# Check memory usage
free -h

# Monitor processes
top
```

---

## Troubleshooting

### Gunicorn not starting

```bash
# Check error
sudo journalctl -u eduflow.service -n 50

# Test manually
cd /opt/eduflow
source venv/bin/activate
gunicorn --workers 3 --bind 127.0.0.1:8000 eduflow_ai.wsgi:application
```

### Nginx errors

```bash
# Test configuration
sudo nginx -t

# Restart
sudo systemctl restart nginx

# Check logs
sudo tail -f /var/log/nginx/error.log
```

### Database connection errors

```bash
# Check database file exists
ls -la /opt/eduflow/db.sqlite3

# Check permissions
sudo chown www-data:www-data /opt/eduflow/db.sqlite3

# Test connection
python manage.py dbshell
```

### SSL certificate issues

```bash
# Check certificate expiry
sudo certbot certificates

# Renew manually
sudo certbot renew

# Check renewal log
sudo tail -f /var/log/letsencrypt/letsencrypt.log
```

---

## Security Best Practices

1. **Change Django SECRET_KEY**
   ```bash
   python manage.py shell
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

2. **Update ALLOWED_HOSTS**
   - Add your domain(s) in settings.py
   - Remove 'localhost' from production

3. **Enable HTTPS**
   - Use Let's Encrypt (automatic with deploy.sh)
   - Set SECURE_SSL_REDIRECT = True

4. **Setup Firewall**
   - Allow only necessary ports (22, 80, 443)
   - Use fail2ban for brute force protection

5. **Regular Updates**
   ```bash
   sudo apt update && sudo apt upgrade -y
   pip install --upgrade -r requirements.txt
   ```

6. **Database Backups**
   - Automated daily backups
   - Test restore procedures
   - Store backups securely

7. **Monitoring**
   - Check logs regularly
   - Set up uptime monitoring
   - Enable error tracking (Sentry)

---

## Support & Documentation

- [Django Documentation](https://docs.djangoproject.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions](https://docs.github.com/en/actions)

For project-specific issues, check the main README.md in the repository.
