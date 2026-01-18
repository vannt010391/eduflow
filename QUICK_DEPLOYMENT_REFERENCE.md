# 🚀 Eduflow Deployment - Quick Reference Card

## **OPTION 1: Ubuntu 24.04 (Easiest)**

```bash
# SSH to your Ubuntu server
ssh user@your-server-ip

# Run one command
sudo bash deploy.sh yourdomain.com admin@yourdomain.com

# Wait 5-10 minutes
# Done! Visit https://yourdomain.com
```

✅ **Includes:** Nginx, Gunicorn, SSL, Backups, Firewall, Security

---

## **OPTION 2: Docker (Most Flexible)**

```bash
# Clone project
git clone --branch feature/update-function https://github.com/vannt010391/eduflow.git
cd eduflow

# Configure
cp .env.example .env
nano .env  # Update settings

# Deploy
docker-compose up -d

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Visit http://localhost
```

✅ **Includes:** Web, Nginx, PostgreSQL, Redis, SSL ready

---

## **OPTION 3: GitHub Actions (Fully Automated)**

```bash
# 1. Add GitHub Secrets:
# HOST, USERNAME, SSH_KEY, PORT

# 2. Push to main branch
git push origin main

# 3. GitHub Actions deploys automatically
# Check: Actions tab in GitHub
```

✅ **Includes:** Auto tests, Auto deploy, Slack alerts

---

## **Common Commands**

### Ubuntu
```bash
# View logs
sudo journalctl -u eduflow.service -f

# Restart
sudo systemctl restart eduflow.service

# Backup
cp /opt/eduflow/db.sqlite3 /backups/eduflow/backup_$(date +%Y%m%d).sqlite3

# Update
cd /opt/eduflow && git pull && pip install -r requirements.txt
python manage.py migrate && sudo systemctl restart eduflow.service
```

### Docker
```bash
# View logs
docker-compose logs -f web

# Restart
docker-compose restart

# Backup
docker-compose exec db pg_dump -U eduflow_user eduflow > backup.sql

# Update
git pull && docker-compose build && docker-compose up -d
```

---

## **Configuration (.env)**

```env
# Essential
SECRET_KEY=your-generated-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=eduflow
DB_USER=eduflow_user
DB_PASSWORD=secure_password

# Email
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=your-app-password

# AI
CLAUDE_API_KEY=sk-ant-api03-xxxxx
```

---

## **Verification**

```bash
# Check setup
bash verify_setup.sh

# Test Django
python manage.py check

# Test database
python manage.py dbshell
```

---

## **Troubleshooting**

| Issue | Solution |
|-------|----------|
| **Can't connect** | Check firewall: `sudo ufw status` |
| **App won't start** | Check logs: `journalctl -u eduflow -n 50` |
| **Database error** | Check permissions: `ls -l /opt/eduflow/db.sqlite3` |
| **SSL issues** | Check cert: `sudo certbot certificates` |
| **Docker won't start** | Check disk space: `df -h` |

---

## **File Locations**

| Item | Ubuntu | Docker |
|------|--------|--------|
| App | `/opt/eduflow` | `/app` |
| Static | `/opt/eduflow/staticfiles` | `/app/staticfiles` |
| Database | `/opt/eduflow/db.sqlite3` | In PostgreSQL container |
| Backups | `/backups/eduflow/` | Manual backup needed |
| Logs | `/var/log/nginx` | `docker-compose logs` |
| Config | `.env` | `.env` |

---

## **Post-Deployment**

- [ ] Create superuser
- [ ] Visit `/admin` to log in
- [ ] Configure domain/DNS
- [ ] Test all features
- [ ] Set up email alerts
- [ ] Configure backups
- [ ] Enable monitoring

---

## **Resources**

📖 Full guides: See `DEPLOYMENT_*.md` files  
🐧 Ubuntu guide: `DEPLOYMENT_UBUNTU_24.04.md`  
🐳 Docker guide: Check `docker-compose.yml`  
🔄 CI/CD guide: Check `.github/workflows/`  
📋 Complete guide: `DEPLOYMENT_COMPLETE_GUIDE.md`  

---

## **Support**

- Check deployment guide for your option
- Review troubleshooting section
- Check application logs
- Consult Django/Nginx documentation

---

**Choose one option above and get started! 🎯**

Need help? See the full deployment guides in the repository.
