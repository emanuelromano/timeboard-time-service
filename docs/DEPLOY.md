# Deployment Guide

This document provides a concise guide for deploying the **TimeBoard Time Service (TBTS)** on a clean Ubuntu Server.

For a complete explanation of the architecture, configuration and operational procedures, refer to the project's Infrastructure Manual.

The deployment uses the following components:

- Ubuntu Server LTS
- Python 3
- Flask
- Gunicorn
- Nginx
- systemd
- UFW Firewall
- Cloudflare (DNS / Proxy)

---

# 1. Update the System

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

# 3. Configure the Firewall

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

source .venv/bin/activate

pip install --upgrade pip

pip install -r requirements.txt
```

---

# 6. Test the Application

Run the application locally.

```bash
python app.py
```

Or test Gunicorn.

```bash
gunicorn -c gunicorn.conf.py app:app
```

The application should be reachable at:

```
http://127.0.0.1:8000
```

---

# 7. Configure Nginx

Copy the project's Nginx configuration files to:

```
/etc/nginx/sites-available/
```

Enable the required sites.

```bash
sudo ln -s /etc/nginx/sites-available/portfolio.conf /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/tbts.conf /etc/nginx/sites-enabled/
```

Remove the default site.

```bash
sudo rm -f /etc/nginx/sites-enabled/default
```

Verify the configuration.

```bash
sudo nginx -t
```

Reload Nginx.

```bash
sudo systemctl reload nginx
```

---

# 8. Configure systemd

Copy the provided service file to:

```
/etc/systemd/system/timeboard-time-service.service
```

Reload systemd.

```bash
sudo systemctl daemon-reload
```

Enable and start the service.

```bash
sudo systemctl enable timeboard-time-service
sudo systemctl start timeboard-time-service
```

Verify:

```bash
sudo systemctl status timeboard-time-service
```

---

# 9. Logs

Follow the service logs.

```bash
journalctl -u timeboard-time-service -f
```

View the latest log entries.

```bash
journalctl -u timeboard-time-service -n 100
```

---

# 10. Updating the Service

```bash
cd /opt/timeboard-time-service

git pull

source .venv/bin/activate

pip install -r requirements.txt

sudo systemctl restart timeboard-time-service
```

---

# Notes

- The personal portfolio is served over HTTPS using Let's Encrypt certificates.
- TBTS intentionally remains available over HTTP for compatibility with Palm OS clients.
- Cloudflare manages DNS for the published domains.

---

# Architecture

```
               Internet
                   │
                   ▼
            Cloudflare DNS/Proxy
                   │
                   ▼
               Nginx
          ┌────────┴────────┐
          ▼                 ▼
   Portfolio (HTTPS)   TBTS (HTTP)
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