# Oracle Cloud Free Tier - Web Server Setup Guide

Complete guide to deploy a secure Linux web server for Python web applications with HTTPS support.

---

## Part 1: Create Oracle Cloud Instance

### 1.1 Create Compute Instance

1. Log in to [Oracle Cloud Console](https://cloud.oracle.com)
2. Navigate to **Compute** → **Instances** → **Create Instance**
3. Configure instance:
   - **Name**: `web-server` (or your choice)
   - **Image**: Ubuntu 22.04 (recommended) or Oracle Linux 8
   - **Shape**: VM.Standard.E2.1.Micro (Always Free eligible)
   - **Network**: Use default VCN or create new
   - **Add SSH keys**: 
     - Select "Paste public keys" or "Generate a key pair"
     - If generating, download both private and public keys immediately
     - Save private key as `~/.ssh/oracle_web_server.key`
4. Click **Create**
5. Note the **Public IP address** once instance is running

### 1.2 Set SSH Key Permissions (Local Machine)

```bash
chmod 600 ~/.ssh/oracle_web_server.key
```

---

## Part 2: Configure Network Security

### 2.1 Configure Security List (Oracle Cloud Console)

1. Navigate to **Networking** → **Virtual Cloud Networks**
2. Click your VCN → **Security Lists** → **Default Security List**
3. Click **Add Ingress Rules** and add:

**Rule 1 - HTTP:**
- Source CIDR: `0.0.0.0/0`
- IP Protocol: TCP
- Destination Port Range: `80`
- Description: `HTTP`

**Rule 2 - HTTPS:**
- Source CIDR: `0.0.0.0/0`
- IP Protocol: TCP
- Destination Port Range: `443`
- Description: `HTTPS`

**Rule 3 - SSH (Recommended: Restrict to your IP):**
- Source CIDR: `YOUR_IP/32` (or `0.0.0.0/0` for any IP)
- IP Protocol: TCP
- Destination Port Range: `22`
- Description: `SSH`

### 2.2 Configure OS Firewall (On Server)

SSH into your instance:

```bash
ssh -i ~/.ssh/oracle_web_server.key ubuntu@YOUR_PUBLIC_IP
```

**For Ubuntu:**

```bash
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo netfilter-persistent save
```

**For Oracle Linux:**

```bash
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

---

## Part 3: Server Initial Setup

### 3.1 Update System

```bash
sudo apt update && sudo apt upgrade -y
```

### 3.2 Install Required Packages

```bash
sudo apt install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx git
```

### 3.3 Configure SSH Security

Edit SSH config:

```bash
sudo nano /etc/ssh/sshd_config
```

Ensure these settings:

```
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
```

Restart SSH:

```bash
sudo systemctl restart sshd
```

### 3.4 Create Application User

```bash
sudo useradd -m -s /bin/bash webapp
sudo usermod -aG sudo webapp
```

---

## Part 4: Setup Domain and HTTPS

### 4.1 Configure Oracle Domain (Optional)

Oracle provides a free subdomain for your instance:

1. In Oracle Console, go to your instance
2. Click **Attached VNICs** → Primary VNIC
3. Click **IP Addresses** → Public IP
4. Note the DNS name (format: `xxx.xxx.xxx.xxx.oraclecloud.com`)

Or use your own domain by pointing A record to your instance's public IP.

### 4.2 Configure Nginx

Create Nginx config:

```bash
sudo nano /etc/nginx/sites-available/webapp
```

Add configuration:

```nginx
server {
    listen 80;
    server_name YOUR_DOMAIN_OR_IP;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/webapp/app/static;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/webapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 4.3 Install SSL Certificate (Let's Encrypt)

```bash
sudo certbot --nginx -d YOUR_DOMAIN
```

Follow prompts:
- Enter email address
- Agree to terms
- Choose redirect option (recommended: redirect HTTP to HTTPS)

Certificate auto-renewal is configured automatically. Test renewal:

```bash
sudo certbot renew --dry-run
```

---

## Part 5: Deploy Python Application

### 5.1 Setup Application Directory

```bash
sudo mkdir -p /home/webapp/app
sudo chown webapp:webapp /home/webapp/app
```

### 5.2 Create Python Virtual Environment

```bash
sudo -u webapp python3 -m venv /home/webapp/app/venv
```

### 5.3 Example Flask Application

Create sample app:

```bash
sudo -u webapp nano /home/webapp/app/app.py
```

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Hello from Oracle Cloud!</h1>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

Install Flask:

```bash
sudo -u webapp /home/webapp/app/venv/bin/pip install flask gunicorn
```

### 5.4 Create Systemd Service

```bash
sudo nano /etc/systemd/system/webapp.service
```

```ini
[Unit]
Description=Web Application
After=network.target

[Service]
User=webapp
Group=webapp
WorkingDirectory=/home/webapp/app
Environment="PATH=/home/webapp/app/venv/bin"
ExecStart=/home/webapp/app/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 app:app

[Install]
WantedBy=multi-user.target
```

Enable and start service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable webapp
sudo systemctl start webapp
sudo systemctl status webapp
```

---

## Part 6: Security Hardening

### 6.1 Configure UFW (Alternative Firewall)

```bash
sudo apt install ufw
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 6.2 Install Fail2Ban

```bash
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 6.3 Automatic Security Updates

```bash
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

---

## Part 7: Maintenance Commands

### Check Application Status

```bash
sudo systemctl status webapp
```

### View Application Logs

```bash
sudo journalctl -u webapp -f
```

### Restart Services

```bash
sudo systemctl restart webapp
sudo systemctl restart nginx
```

### Renew SSL Certificate Manually

```bash
sudo certbot renew
```

### Update System

```bash
sudo apt update && sudo apt upgrade -y
```

---

## Part 8: Deployment Workflow

### Deploy New Code

```bash
# SSH into server
ssh -i ~/.ssh/oracle_web_server.key ubuntu@YOUR_PUBLIC_IP

# Navigate to app directory
cd /home/webapp/app

# Pull latest code (if using git)
sudo -u webapp git pull

# Install dependencies
sudo -u webapp /home/webapp/app/venv/bin/pip install -r requirements.txt

# Restart application
sudo systemctl restart webapp
```

---

## Troubleshooting

### Cannot Connect via SSH
- Check Security List allows port 22 from your IP
- Verify key permissions: `chmod 600 ~/.ssh/oracle_web_server.key`
- Check instance is running in Oracle Console

### Cannot Access Website
- Verify Security List allows ports 80 and 443
- Check firewall: `sudo iptables -L -n`
- Check Nginx: `sudo systemctl status nginx`
- Check application: `sudo systemctl status webapp`

### SSL Certificate Issues
- Ensure domain points to correct IP
- Check Nginx config: `sudo nginx -t`
- View Certbot logs: `sudo certbot certificates`

### Application Not Running
- Check logs: `sudo journalctl -u webapp -n 50`
- Verify Python environment: `sudo -u webapp /home/webapp/app/venv/bin/python --version`
- Test manually: `sudo -u webapp /home/webapp/app/venv/bin/python /home/webapp/app/app.py`

---

## Additional Resources

- [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

---

## Summary

You now have:
- ✅ Secure Linux server on Oracle Cloud Free Tier
- ✅ SSH access with key-based authentication
- ✅ Firewall configured (cloud and OS level)
- ✅ Nginx reverse proxy
- ✅ HTTPS with Let's Encrypt SSL
- ✅ Python application with systemd service
- ✅ Automatic security updates
- ✅ Fail2Ban protection

Your application is accessible at: `https://YOUR_DOMAIN`
