# Deployment Guide

This document describes how to deploy the **TimeBoard Time Service (TBTS)** on a clean Ubuntu server.

The deployment uses the following components:

- Ubuntu Server
- Python 3
- Flask
- Gunicorn
- Nginx
- systemd
- UFW firewall

---

# 1. System Update

Update the operating system.

```bash
sudo apt update
sudo apt full-upgrade
sudo reboot
```

---

# 2. Install Required Packages

```bash
sudo apt install python3 python3-venv python3-pip nginx git ufw
```

---

# 3. Configure Firewall

Allow SSH and HTTP traffic.

```bash
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

Verify:

```bash
sudo ufw status
```

---

# 4. Clone the Repository

```bash
cd /opt

sudo mkdir timeboard-time-service
sudo chown $USER:$USER timeboard-time-service

cd timeboard-time-service

git clone git@github.com:emanuelromano/timeboard-time-service.git .
```

---

# 5. Create the Python Virtual Environment

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Upgrade pip:

```bash
pip install --upgrade pip
```

Install project dependencies:

```bash
pip install -r requirements.txt
```

---

# 6. Test the Application

Run the application manually.

```bash
python app.py
```

Or test Gunicorn directly.

```bash
gunicorn -c gunicorn.conf.py app:app
```

The API should be available on:

```
http://127.0.0.1:8000
```

---

# 7. Configure Nginx

Create:

```
/etc/nginx/sites-available/timeboard-time-service
```

Example configuration:

```nginx
server {

    listen 80 default_server;

    server_name _;

    location / {

        proxy_pass http://127.0.0.1:8000;

        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header Connection "";
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

    }

}
```

Enable the site.

```bash
sudo ln -s /etc/nginx/sites-available/timeboard-time-service \
           /etc/nginx/sites-enabled/
```

Remove the default site.

```bash
sudo rm -f /etc/nginx/sites-enabled/default
```

Test the configuration.

```bash
sudo nginx -t
```

Reload Nginx.

```bash
sudo systemctl reload nginx
```

---

# 8. Configure systemd

Create:

```
/etc/systemd/system/timeboard-time-service.service
```

Example:

```ini
[Unit]
Description=TimeBoard Time Service (TBTS)
After=network.target

[Service]

Type=simple

User=roadie
Group=roadie

WorkingDirectory=/opt/timeboard-time-service

Environment="PATH=/opt/timeboard-time-service/.venv/bin"

ExecStart=/opt/timeboard-time-service/.venv/bin/gunicorn \
    -c /opt/timeboard-time-service/gunicorn.conf.py \
    app:app

Restart=always
RestartSec=5

NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
ProtectHome=true

[Install]
WantedBy=multi-user.target
```

Reload systemd.

```bash
sudo systemctl daemon-reload
```

Enable the service.

```bash
sudo systemctl enable timeboard-time-service
```

Start the service.

```bash
sudo systemctl start timeboard-time-service
```

Check status.

```bash
sudo systemctl status timeboard-time-service
```

---

# 9. Logs

View live logs.

```bash
journalctl -u timeboard-time-service -f
```

View the last 100 log lines.

```bash
journalctl -u timeboard-time-service -n 100
```

---

# 10. Updating the Service

Pull the latest changes.

```bash
cd /opt/timeboard-time-service

git pull
```

If dependencies changed:

```bash
source .venv/bin/activate

pip install -r requirements.txt
```

Restart the service.

```bash
sudo systemctl restart timeboard-time-service
```

---

# Architecture

```
Internet
    │
    ▼
 Nginx (80)
    │
    ▼
Gunicorn
    │
    ▼
Flask
    │
    ▼
TimeBoard Time Service
```