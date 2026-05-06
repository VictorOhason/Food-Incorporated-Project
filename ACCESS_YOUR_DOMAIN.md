# How to Access Your Live Code on Your Domain

Your Food Incorporated application is now configured for domain access. Here's how to access it:

## Quick Access URLs

Once deployed to your domain `s2330027.ncgrp.xyz`:

```
Frontend (Customer Menu):  https://s2330027.ncgrp.xyz/Menu/menu.html
Admin Login:               https://s2330027.ncgrp.xyz/Admin_Login/index.html
API Health:                https://s2330027.ncgrp.xyz/health
```

---

## Step-by-Step Deployment

### 1. Development Testing (Local)

**Start the Flask Backend:**
```bash
cd "Food incorporated/Kitchen_app"
python3 server.py
```
You should see: `Running on http://localhost:5000`

**In another terminal, start the Frontend:**
```bash
cd "Food incorporated"
python3 -m http.server 8000
```
You should see: `Serving HTTP on 0.0.0.0 port 8000`

**Access locally:**
- Menu: `http://localhost:8000/Menu/menu.html`
- Admin: `http://localhost:8000/Admin_Login/index.html`

---

### 2. Deploy to Your Domain (Production)

#### Option A: Using Nginx (Recommended)

**1. Create Nginx configuration file:**
```bash
sudo nano /etc/nginx/sites-available/foodinc
```

**2. Add this configuration:**
```nginx
upstream flask_app {
    server localhost:5000;
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name s2330027.ncgrp.xyz;
    return 301 https://$server_name$request_uri;
}

# HTTPS Server
server {
    listen 443 ssl http2;
    server_name s2330027.ncgrp.xyz;

    # SSL Certificate (obtain from your hosting provider)
    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;

    # Serve frontend files
    location / {
        root /home/ncgrp-s2330027/Food-Incorporated-Project/Food\ incorporated;
        try_files $uri $uri/ =404;
    }

    # Proxy API requests to Flask backend
    location /orders {
        proxy_pass http://flask_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /stock {
        proxy_pass http://flask_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /tables {
        proxy_pass http://flask_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /health {
        proxy_pass http://flask_app;
        proxy_set_header Host $host;
    }
}
```

**3. Enable the site:**
```bash
sudo ln -s /etc/nginx/sites-available/foodinc /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

**4. Start Flask backend (from your server):**
```bash
cd /home/ncgrp-s2330027/Food-Incorporated-Project/Food\ incorporated/Kitchen_app
gunicorn server:app --bind 0.0.0.0:5000 --workers 4
```

Or use a process manager like systemd:
```bash
sudo nano /etc/systemd/system/foodinc.service
```

Add:
```ini
[Unit]
Description=Food Incorporated Flask App
After=network.target

[Service]
User=ncgrp-s2330027
WorkingDirectory=/home/ncgrp-s2330027/Food-Incorporated-Project/Food incorporated/Kitchen_app
ExecStart=/usr/bin/python3 -m gunicorn server:app --bind 0.0.0.0:5000

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable foodinc
sudo systemctl start foodinc
sudo systemctl status foodinc
```

---

#### Option B: Using Apache

**1. Enable mod_proxy:**
```bash
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod ssl
sudo a2enmod rewrite
```

**2. Create VirtualHost:**
```bash
sudo nano /etc/apache2/sites-available/foodinc.conf
```

**3. Add configuration:**
```apache
<VirtualHost *:443>
    ServerName s2330027.ncgrp.xyz
    ServerAdmin admin@example.com

    SSLEngine on
    SSLCertificateFile /path/to/certificate.crt
    SSLCertificateKeyFile /path/to/private.key

    # Serve static files
    DocumentRoot /home/ncgrp-s2330027/Food-Incorporated-Project/Food\ incorporated

    # Proxy API requests
    ProxyPreserveHost On
    ProxyPass /orders http://localhost:5000/orders
    ProxyPassReverse /orders http://localhost:5000/orders
    ProxyPass /stock http://localhost:5000/stock
    ProxyPassReverse /stock http://localhost:5000/stock
    ProxyPass /tables http://localhost:5000/tables
    ProxyPassReverse /tables http://localhost:5000/tables

    # Error and access logs
    ErrorLog ${APACHE_LOG_DIR}/foodinc_error.log
    CustomLog ${APACHE_LOG_DIR}/foodinc_access.log combined
</VirtualHost>

# Redirect HTTP to HTTPS
<VirtualHost *:80>
    ServerName s2330027.ncgrp.xyz
    Redirect permanent / https://s2330027.ncgrp.xyz/
</VirtualHost>
```

**4. Enable site:**
```bash
sudo a2ensite foodinc
sudo apache2ctl configtest
sudo systemctl restart apache2
```

---

### 3. Update Environment Variables for Production

Your `.env` is already configured, but verify it's correct:

```bash
cat /home/ncgrp-s2330027/Food-Incorporated-Project/Food\ incorporated/Kitchen_app/.env
```

Should show:
```env
API_PROTOCOL=https
API_HOST=s2330027.ncgrp.xyz
API_PORT=443
ALLOWED_ORIGINS=https://s2330027.ncgrp.xyz,http://localhost:8000
```

---

## Testing Your Domain Access

### 1. Test Frontend Load
```bash
curl https://s2330027.ncgrp.xyz/Menu/menu.html
```
Should return HTML content

### 2. Test API Health
```bash
curl https://s2330027.ncgrp.xyz/health
```
Should return:
```json
{"status": "healthy", "message": "Server is running"}
```

### 3. Test in Browser
Open browser and go to:
```
https://s2330027.ncgrp.xyz/Menu/menu.html
```

Open DevTools (F12) and check console:
```javascript
CONFIG.API_URL
// Should return: https://s2330027.ncgrp.xyz
```

### 4. Test Order Flow
1. Place an order on the menu
2. Check Network tab in DevTools
3. API calls should go to `https://s2330027.ncgrp.xyz/orders`

---

## Running Desktop App Against Live Domain

Once deployed, the desktop kitchen app automatically connects to your domain:

```bash
cd "Food incorporated"
python3 Kitchen_app/app.py
```

It will automatically use:
```
API URL: https://s2330027.ncgrp.xyz:443
```

No need to change anything!

---

## Troubleshooting

### Issue: "Connection Refused"
**Solution:** Check Flask backend is running
```bash
sudo systemctl status foodinc
# or
ps aux | grep gunicorn
```

### Issue: "Bad Gateway" 504
**Solution:** Nginx/Apache can't reach Flask
```bash
# Check Flask is listening on port 5000
netstat -tuln | grep 5000
```

### Issue: CORS Error
**Solution:** Verify domain in .env
```bash
grep ALLOWED_ORIGINS /path/to/.env
```

### Issue: SSL Certificate Error
**Solution:** Install valid certificate (Let's Encrypt recommended)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d s2330027.ncgrp.xyz
```

---

## Quick Reference

| Service | Command | Port |
|---------|---------|------|
| Frontend | `python3 -m http.server 8000` | 8000 |
| Flask Backend | `python3 server.py` | 5000 |
| Nginx | `sudo systemctl restart nginx` | 80/443 |
| Gunicorn | `gunicorn server:app --bind 0.0.0.0:5000` | 5000 |

---

## Summary

Your application now:
- ✅ Uses your domain instead of hardcoded IP
- ✅ Automatically detects your domain in frontend
- ✅ Reads domain from environment variables in backend
- ✅ Has security headers configured
- ✅ Is ready for production deployment

**To go live, just:**
1. Set up Nginx/Apache reverse proxy
2. Start Flask backend with gunicorn
3. Access via `https://s2330027.ncgrp.xyz`
