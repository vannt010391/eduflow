# Eduflow Deployment Complete Setup

This directory contains all necessary files and configurations for deploying Eduflow to production on Ubuntu 24.04 with multiple deployment options.

## 📋 What's Included

### Deployment Scripts & Configuration

1. **deploy.sh** - Fully automated deployment script
   - One-command deployment to Ubuntu 24.04
   - Handles all configuration and setup
   - Installs: Python, Nginx, Gunicorn, Certbot, Firewall
   - Sets up backups, SSL, and security

2. **Dockerfile** - Docker image for containerized deployment
   - Multi-stage Python 3.11 image
   - Health checks included
   - Non-root user for security

3. **docker-compose.yml** - Complete Docker stack
   - Web (Django/Gunicorn)
   - Nginx (Reverse proxy)
   - PostgreSQL (Database)
   - Redis (Cache/Sessions)

4. **nginx.conf** - Production-ready Nginx configuration
   - SSL/TLS support
   - Gzip compression
   - Security headers
   - Proper proxy settings

5. **.env.example** - Environment variables template
   - Django settings
   - Database configuration
   - Email settings
   - AI/Claude API keys

### CI/CD Pipelines

1. **.github/workflows/tests.yml**
   - Automated testing on push/PR
   - Python 3.9, 3.10, 3.11
   - Code coverage
   - Security scanning
   - Code quality checks

2. **.github/workflows/deploy.yml**
   - Automated deployment to production
   - Docker deployment option
   - Slack notifications
   - SSH deployment to Ubuntu server

### Documentation

1. **DEPLOYMENT_UBUNTU_24.04.md** - Traditional deployment guide
   - Step-by-step manual instructions
   - System configuration
   - Service management
   - Troubleshooting

2. **DEPLOYMENT_COMPLETE_GUIDE.md** - Comprehensive guide
   - All 3 deployment options
   - Configuration examples
   - Maintenance procedures
   - Security best practices

### Verification & Setup

1. **verify_setup.sh** - Setup verification script
   - Checks all components
   - Validates configuration
   - Reports missing items

2. **.dockerignore** - Docker build exclusions
   - Optimizes image size
   - Excludes unnecessary files

## 🚀 Quick Start

### Option 1: Automated Ubuntu 24.04 (Recommended for Beginners)

```bash
# SSH to your Ubuntu server
ssh user@your-server-ip

# Download and run deployment script
wget https://raw.githubusercontent.com/vannt010391/eduflow/feature/update-function/deploy.sh
sudo bash deploy.sh yourdomain.com admin@yourdomain.com
```

**That's it!** The script handles everything automatically.

**What gets installed:**
- ✅ Python 3 + dependencies
- ✅ Nginx web server
- ✅ Gunicorn app server
- ✅ PostgreSQL (optional) or SQLite
- ✅ SSL certificate (Let's Encrypt)
- ✅ Firewall configuration
- ✅ Automated backups
- ✅ Security hardening

### Option 2: Docker Deployment (Best for Development/Production)

```bash
# Clone project
git clone --branch feature/update-function https://github.com/vannt010391/eduflow.git
cd eduflow

# Configure environment
cp .env.example .env
nano .env  # Update your settings

# Start services
docker-compose up -d

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access application
open http://localhost
```

### Option 3: GitHub Actions CI/CD (Fully Automated)

1. Push code to main branch
2. GitHub Actions automatically:
   - Runs tests
   - Builds Docker images
   - Deploys to production
   - Sends Slack notifications

## 📝 Configuration Files

### .env Template
```env
# Copy .env.example to .env and update:
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@localhost/dbname
CLAUDE_API_KEY=your-claude-api-key
EMAIL_HOST_USER=your-email@gmail.com
```

## 🔍 Verification

Before deployment, run:

```bash
bash verify_setup.sh
```

This checks:
- Python installation
- Required files
- Environment configuration
- Docker setup
- Git configuration

## 📊 Deployment Comparison

| Feature | Ubuntu Script | Docker | CI/CD |
|---------|---------------|--------|-------|
| Setup Time | 5-10 min | 2-3 min | Automated |
| SSL/TLS | ✅ Auto | Manual | ✅ Auto |
| Backups | ✅ Daily | Manual | ✅ Daily |
| Scaling | ❌ Manual | ✅ Easy | ✅ Auto |
| Monitoring | ✅ Logs | ✅ Logs | ✅ Slack |
| Database | SQLite/Postgres | PostgreSQL | Auto |
| Best For | Production | Dev/Prod | Large Teams |

## 🛠️ Common Tasks

### View Logs

**Ubuntu:**
```bash
sudo journalctl -u eduflow.service -f
sudo tail -f /var/log/nginx/error.log
```

**Docker:**
```bash
docker-compose logs -f web
docker-compose logs -f nginx
```

### Update Application

**Ubuntu:**
```bash
cd /opt/eduflow
git pull origin feature/update-function
source venv/bin/activate
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

### Database Backup

**Ubuntu:**
```bash
cp /opt/eduflow/db.sqlite3 /backups/eduflow/backup_$(date +%Y%m%d).sqlite3
```

**Docker:**
```bash
docker-compose exec db pg_dump -U eduflow_user eduflow > backup.sql
```

## 🔐 Security Checklist

- [ ] Change Django SECRET_KEY
- [ ] Update ALLOWED_HOSTS with your domain
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Set DEBUG=False in production
- [ ] Configure secure cookie settings
- [ ] Set up database backups
- [ ] Enable monitoring/logging
- [ ] Configure email for alerts

## 🆘 Troubleshooting

### Gunicorn not starting
```bash
sudo journalctl -u eduflow.service -n 50
cd /opt/eduflow && source venv/bin/activate
gunicorn --workers 3 --bind 127.0.0.1:8000 eduflow_ai.wsgi:application
```

### Nginx errors
```bash
sudo nginx -t
sudo systemctl restart nginx
sudo tail -f /var/log/nginx/error.log
```

### Database connection issues
```bash
python manage.py dbshell
```

### Docker issues
```bash
docker-compose down
docker-compose up -d
docker-compose logs web
```

## 📚 Documentation

- [DEPLOYMENT_UBUNTU_24.04.md](DEPLOYMENT_UBUNTU_24.04.md) - Traditional deployment
- [DEPLOYMENT_COMPLETE_GUIDE.md](DEPLOYMENT_COMPLETE_GUIDE.md) - All options
- [README.md](README.md) - Project overview

## 🌍 Deployment Checklist

### Pre-Deployment
- [ ] Review .env.example
- [ ] Generate SECRET_KEY
- [ ] Configure database
- [ ] Set up email
- [ ] Configure AI/Claude API
- [ ] Test locally with `python manage.py runserver`

### Deployment
- [ ] Choose deployment option
- [ ] Follow specific guide
- [ ] Verify installation with `verify_setup.sh`
- [ ] Create superuser
- [ ] Access admin panel
- [ ] Configure domain/DNS

### Post-Deployment
- [ ] Enable HTTPS
- [ ] Configure backups
- [ ] Set up monitoring
- [ ] Test all features
- [ ] Configure Slack notifications
- [ ] Document any customizations

## 📞 Support

- Check individual deployment guides for detailed instructions
- Review troubleshooting sections
- Check logs for error messages
- Consult Django/Nginx documentation

## 🎯 Next Steps

1. Choose your deployment option above
2. Follow the corresponding guide
3. Run verification script
4. Monitor deployment
5. Configure post-deployment items

## 📄 License

See LICENSE file in repository.

---

**Happy Deploying! 🚀**

For more information, see the detailed deployment guides in this directory.
