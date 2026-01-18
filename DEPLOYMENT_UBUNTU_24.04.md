# Deployment Guide: Ubuntu 24.04 with Nginx and SQLite

## Prerequisites
- Ubuntu 24.04 LTS installed and updated
- SSH access to the server
- Domain name (optional but recommended)

## Step 1: Update System
```bash
sudo apt update
sudo apt upgrade -y
```

## Step 2: Install Python and Required Dependencies
```bash
sudo apt install -y python3 python3-pip python3-venv git nginx curl
```

## Step 3: Clone Project from GitHub
```bash
cd /opt
sudo git clone https://github.com/vannt010391/eduflow.git
sudo chown -R $USER:$USER /opt/eduflow
cd /opt/eduflow
```

## Step 4: Create Python Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

## Step 5: Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 6: Configure Django Project
```bash
# Create .env file
cp .env.example .env
nano .env  # Edit with your settings

# Update settings.py for production
# Change DEBUG = False
# Add ALLOWED_HOSTS = ['your_domain.com', 'www.your_domain.com', 'server_ip']
```

## Step 7: Run Django Migrations
```bash
python manage.py migrate
```

## Step 8: Create Superuser
```bash
python manage.py createsuperuser
```

## Step 9: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

## Step 10: Install and Configure Gunicorn
```bash
pip install gunicorn
```

### Create Gunicorn Systemd Service
```bash
sudo nano /etc/systemd/system/eduflow.service
```

Add the following content:
```ini
[Unit]
Description=Eduflow Django Application
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/eduflow
Environment="PATH=/opt/eduflow/venv/bin"
ExecStart=/opt/eduflow/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 --timeout 60 eduflow_ai.wsgi:application
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable eduflow.service
sudo systemctl start eduflow.service
sudo systemctl status eduflow.service
```

## Step 11: Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/eduflow
```

Add the following configuration:
```nginx
upstream eduflow_app {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    listen [::]:80;
    server_name your_domain.com www.your_domain.com;

    client_max_body_size 20M;

    location /static/ {
        alias /opt/eduflow/static/;
    }

    location /media/ {
        alias /opt/eduflow/media/;
    }

    location / {
        proxy_pass http://eduflow_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/eduflow /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

## Step 12: Set Up SSL with Let's Encrypt (Recommended)
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your_domain.com -d www.your_domain.com
```

### Auto-renewal
```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

## Step 13: Configure Firewall
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## Step 14: Set Up Database Backups (SQLite)
```bash
sudo mkdir -p /backups/eduflow
sudo chown www-data:www-data /backups/eduflow
```

Create backup script:
```bash
sudo nano /usr/local/bin/backup-eduflow.sh
```

Add:
```bash
#!/bin/bash
BACKUP_DIR="/backups/eduflow"
DB_PATH="/opt/eduflow/db.sqlite3"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

cp $DB_PATH $BACKUP_DIR/db_backup_$TIMESTAMP.sqlite3
find $BACKUP_DIR -name "db_backup_*.sqlite3" -mtime +7 -delete
```

Make it executable and add to cron:
```bash
sudo chmod +x /usr/local/bin/backup-eduflow.sh
sudo crontab -e
```

Add line:
```
0 2 * * * /usr/local/bin/backup-eduflow.sh
```

## Step 15: Verify Deployment
```bash
# Check Gunicorn service
sudo systemctl status eduflow.service

# Check Nginx
sudo systemctl status nginx

# Test the application
curl http://127.0.0.1:8000
```

## Monitoring and Maintenance

### View logs
```bash
# Django/Gunicorn logs
sudo journalctl -u eduflow.service -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Update project
```bash
cd /opt/eduflow
source venv/bin/activate
git pull origin feature/update-function
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart eduflow.service
```

## Troubleshooting

### Permission Issues
```bash
sudo chown -R www-data:www-data /opt/eduflow
```

### Gunicorn not starting
```bash
cd /opt/eduflow
source venv/bin/activate
gunicorn --workers 3 --bind 127.0.0.1:8000 eduflow_ai.wsgi:application
```

### Nginx errors
```bash
sudo nginx -t
sudo systemctl restart nginx
```

### Check connectivity
```bash
sudo netstat -tlnp | grep 8000
sudo netstat -tlnp | grep 80
```

## Security Hardening

1. Keep system updated:
```bash
sudo apt update && sudo apt upgrade -y
```

2. Configure fail2ban:
```bash
sudo apt install -y fail2ban
```

3. Disable SSH password login and use key-based auth
4. Change Django SECRET_KEY in .env
5. Set secure cookies in settings.py:
```python
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## Performance Optimization

1. Increase Gunicorn workers based on CPU cores:
```bash
# For 4 CPU cores: workers = (2 * 4) + 1 = 9
```

2. Enable Gzip compression in Nginx:
```nginx
gzip on;
gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss;
gzip_vary on;
gzip_min_length 1024;
```

3. Add caching headers for static files

## Database Backup and Recovery

### Backup
```bash
cp /opt/eduflow/db.sqlite3 /backups/eduflow/db_manual_backup.sqlite3
```

### Restore
```bash
cp /backups/eduflow/db_backup_YYYYMMDD_HHMMSS.sqlite3 /opt/eduflow/db.sqlite3
sudo chown www-data:www-data /opt/eduflow/db.sqlite3
sudo systemctl restart eduflow.service
```

---

## Support
For issues or questions, check the logs and refer to Django/Nginx documentation.
