#!/bin/bash

# Eduflow Deployment Automation Script for Ubuntu 24.04
# Usage: sudo bash deploy.sh [domain] [email]
# Example: sudo bash deploy.sh eduflow.example.com admin@example.com

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
DOMAIN=${1:-"localhost"}
EMAIL=${2:-"admin@example.com"}
APP_DIR="/opt/eduflow"
VENV_DIR="$APP_DIR/venv"
PROJECT_URL="https://github.com/vannt010391/eduflow.git"
BRANCH="feature/update-function"

# Helper functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        log_error "This script must be run as root"
        exit 1
    fi
}

# Step 1: System Update
update_system() {
    log_info "Updating system packages..."
    apt update
    apt upgrade -y
}

# Step 2: Install Dependencies
install_dependencies() {
    log_info "Installing required dependencies..."
    apt install -y python3 python3-pip python3-venv git nginx curl wget \
                   certbot python3-certbot-nginx postgresql postgresql-contrib \
                   fail2ban ufw supervisor
}

# Step 3: Clone Project
clone_project() {
    log_info "Cloning eduflow project..."
    if [ -d "$APP_DIR" ]; then
        log_warn "Directory $APP_DIR already exists. Updating..."
        cd $APP_DIR
        git pull origin $BRANCH
    else
        git clone --branch $BRANCH $PROJECT_URL $APP_DIR
    fi
    chown -R www-data:www-data $APP_DIR
}

# Step 4: Create Virtual Environment
create_venv() {
    log_info "Creating Python virtual environment..."
    cd $APP_DIR
    python3 -m venv $VENV_DIR
    source $VENV_DIR/bin/activate
}

# Step 5: Install Python Dependencies
install_python_deps() {
    log_info "Installing Python dependencies..."
    source $VENV_DIR/bin/activate
    pip install --upgrade pip setuptools wheel
    pip install -r $APP_DIR/requirements.txt
    pip install gunicorn supervisor
}

# Step 6: Configure Django
configure_django() {
    log_info "Configuring Django project..."
    
    cd $APP_DIR
    
    # Create .env if it doesn't exist
    if [ ! -f ".env" ]; then
        cp .env.example .env
        log_warn ".env created - please update it with your settings"
    fi
    
    # Generate Django secret key
    SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
    
    # Update .env with secret key
    sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
    sed -i "s/ALLOWED_HOSTS=.*/ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN,127.0.0.1/" .env
    sed -i "s/DEBUG=.*/DEBUG=False/" .env
}

# Step 7: Run Migrations
run_migrations() {
    log_info "Running Django migrations..."
    source $VENV_DIR/bin/activate
    cd $APP_DIR
    python manage.py migrate
}

# Step 8: Collect Static Files
collect_static() {
    log_info "Collecting static files..."
    source $VENV_DIR/bin/activate
    cd $APP_DIR
    python manage.py collectstatic --noinput
}

# Step 9: Create Superuser
create_superuser() {
    log_info "Creating Django superuser..."
    source $VENV_DIR/bin/activate
    cd $APP_DIR
    python manage.py createsuperuser
}

# Step 10: Configure Gunicorn Systemd Service
configure_gunicorn() {
    log_info "Configuring Gunicorn service..."
    
    cat > /etc/systemd/system/eduflow.service <<EOF
[Unit]
Description=Eduflow Django Application
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=$APP_DIR
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/gunicorn \\
    --workers 3 \\
    --bind 127.0.0.1:8000 \\
    --timeout 60 \\
    --access-logfile - \\
    --error-logfile - \\
    eduflow_ai.wsgi:application
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
    
    systemctl daemon-reload
    systemctl enable eduflow.service
    systemctl start eduflow.service
    log_info "Gunicorn service started"
}

# Step 11: Configure Nginx
configure_nginx() {
    log_info "Configuring Nginx..."
    
    cat > /etc/nginx/sites-available/eduflow <<EOF
upstream eduflow_app {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    listen [::]:80;
    server_name $DOMAIN www.$DOMAIN;

    client_max_body_size 20M;

    location /static/ {
        alias $APP_DIR/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias $APP_DIR/media/;
    }

    location / {
        proxy_pass http://eduflow_app;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
EOF
    
    ln -sf /etc/nginx/sites-available/eduflow /etc/nginx/sites-enabled/
    nginx -t
    systemctl enable nginx
    systemctl restart nginx
    log_info "Nginx configured and restarted"
}

# Step 12: Setup SSL with Let's Encrypt
setup_ssl() {
    log_info "Setting up SSL with Let's Encrypt..."
    
    certbot --nginx -d $DOMAIN -d www.$DOMAIN --email $EMAIL --non-interactive --agree-tos
    
    # Enable auto-renewal
    systemctl enable certbot.timer
    systemctl start certbot.timer
    log_info "SSL certificate installed with auto-renewal"
}

# Step 13: Configure Firewall
setup_firewall() {
    log_info "Configuring firewall..."
    
    ufw allow 22/tcp
    ufw allow 80/tcp
    ufw allow 443/tcp
    ufw --force enable
    log_info "Firewall configured"
}

# Step 14: Setup Database Backups
setup_backups() {
    log_info "Setting up database backups..."
    
    mkdir -p /backups/eduflow
    chown www-data:www-data /backups/eduflow
    
    cat > /usr/local/bin/backup-eduflow.sh <<'BACKUP_EOF'
#!/bin/bash
BACKUP_DIR="/backups/eduflow"
DB_PATH="/opt/eduflow/db.sqlite3"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Create backup
cp $DB_PATH $BACKUP_DIR/db_backup_$TIMESTAMP.sqlite3

# Keep only 30 days of backups
find $BACKUP_DIR -name "db_backup_*.sqlite3" -mtime +30 -delete

echo "Backup completed: db_backup_$TIMESTAMP.sqlite3"
BACKUP_EOF
    
    chmod +x /usr/local/bin/backup-eduflow.sh
    
    # Add to crontab
    (crontab -u www-data -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/backup-eduflow.sh") | crontab -u www-data -
    log_info "Backup scheduled daily at 2 AM"
}

# Step 15: Setup Fail2Ban
setup_fail2ban() {
    log_info "Configuring Fail2Ban..."
    
    systemctl enable fail2ban
    systemctl start fail2ban
    log_info "Fail2Ban enabled"
}

# Step 16: Verify Deployment
verify_deployment() {
    log_info "Verifying deployment..."
    
    echo ""
    log_info "=== Service Status ==="
    systemctl status eduflow.service --no-pager
    echo ""
    
    systemctl status nginx --no-pager
    echo ""
    
    log_info "=== Port Checks ==="
    netstat -tlnp | grep -E ":(80|443|8000)" || true
    echo ""
    
    log_info "=== Testing Application ==="
    curl -I http://127.0.0.1:8000 || true
    echo ""
}

# Main execution
main() {
    log_info "Starting Eduflow Deployment on Ubuntu 24.04"
    log_info "Domain: $DOMAIN"
    log_info "Email: $EMAIL"
    echo ""
    
    check_root
    
    read -p "Continue with deployment? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_warn "Deployment cancelled"
        exit 1
    fi
    
    update_system
    install_dependencies
    clone_project
    create_venv
    install_python_deps
    configure_django
    run_migrations
    collect_static
    create_superuser
    configure_gunicorn
    configure_nginx
    setup_ssl
    setup_firewall
    setup_backups
    setup_fail2ban
    verify_deployment
    
    log_info "Deployment completed successfully!"
    log_info "Application is available at: https://$DOMAIN"
    log_info "Admin panel: https://$DOMAIN/admin"
}

main "$@"
