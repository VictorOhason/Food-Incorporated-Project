# Domain Configuration Guide

This document explains how to configure the Food Incorporated application to work with your domain.

## Overview

The application has been updated to use environment-based configuration instead of hardcoded IP addresses. This allows you to easily switch between development and production environments.

## Frontend Configuration (JavaScript)

### How it Works
1. The frontend automatically detects the current domain from `window.location`
2. API endpoints are constructed dynamically in `config.js`
3. All JavaScript files load the `config.js` file first to ensure API URLs are available

### Configuration File: `config.js`
Location: `/Food incorporated/config.js`

The `config.js` file automatically:
- Detects if running in development (localhost/127.0.0.1) or production
- Uses HTTPS in production, HTTP in development
- Constructs API URLs based on the current domain

**Usage in HTML files:**
```html
<script src="../config.js"></script>
<script src="menu.js"></script>
```

**Usage in JavaScript:**
```javascript
// Automatically available globally after config.js loads
console.log(CONFIG.API_URL);      // Base API URL
console.log(CONFIG.ORDERS_URL);   // /orders endpoint
console.log(CONFIG.TABLES_URL);   // /tables endpoint
console.log(CONFIG.STOCK_URL);    // /stock endpoint
```

## Backend Configuration (Flask/Python)

### Environment Variables (.env file)
Location: `/Food incorporated/Kitchen_app/.env`

Key variables to configure:

```env
# API Base Configuration
API_PROTOCOL=https              # Use https in production
API_HOST=s2330027.ncgrp.xyz     # Your domain
API_PORT=443                    # 443 for HTTPS, 5000 for HTTP dev

# CORS Configuration
ALLOWED_ORIGINS=https://s2330027.ncgrp.xyz,http://localhost:8000

# Database
DATABASE_URL=sqlite:///foodinc.db
# For PostgreSQL: DATABASE_URL=postgresql://user:password@host/dbname

# Security
FLASK_ENV=production
DEBUG=False
SECURE_HSTS_SECONDS=31536000
```

### API Configuration (Python clients)
Location: `/Food incorporated/Kitchen_app/api.py`

The Python API client now reads from environment variables:
```python
API_PROTOCOL = os.getenv('API_PROTOCOL', 'http')
API_HOST = os.getenv('API_HOST', 'localhost')
API_PORT = os.getenv('API_PORT', '5000')
BASE_URL = f"{API_PROTOCOL}://{API_HOST}:{API_PORT}"
```

## Deployment Steps

### 1. Update Environment Variables

Edit `Kitchen_app/.env` with your domain:

```bash
cd "Food incorporated/Kitchen_app"
cat > .env << EOF
API_PROTOCOL=https
API_HOST=your-domain.com
API_PORT=443
ALLOWED_ORIGINS=https://your-domain.com,http://localhost:8000
DATABASE_URL=sqlite:///foodinc.db
FLASK_ENV=production
DEBUG=False
EOF
```

### 2. Install Dependencies

```bash
cd "Kitchen_app"
pip install -r requirements.txt
```

### 3. Initialize Database

```bash
python
>>> from server import app, init_db
>>> init_db()
>>> exit()
```

### 4. Serve Frontend Files

The HTML files in `/Menu` and `/Admin_Login` need to be served via HTTP/HTTPS.

**Option A: Using Python's built-in server (development only)**
```bash
cd "Food incorporated"
python -m http.server 8000
```

**Option B: Using Nginx (production)**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;
    
    # SSL certificates
    ssl_certificate /path/to/cert.crt;
    ssl_certificate_key /path/to/key.key;
    
    # Serve frontend
    location / {
        root /path/to/Food-Incorporated-Project/Food\ incorporated;
        try_files $uri $uri/ =404;
    }
    
    # Proxy API requests to Flask backend
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 5. Start Flask Backend

```bash
cd "Kitchen_app"
gunicorn server:app
```

Or for development:
```bash
python server.py
```

## CORS Configuration

The Flask backend is configured to only accept requests from specified origins. Update `ALLOWED_ORIGINS` in `.env` to include all domains where the frontend is hosted:

```env
ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com,http://localhost:8000
```

## Security Headers

The Flask backend automatically sets security headers:
- `X-Frame-Options`: SAMEORIGIN (prevent clickjacking)
- `X-Content-Type-Options`: nosniff (prevent MIME sniffing)
- `X-XSS-Protection`: 1; mode=block (enable XSS protection)
- `Strict-Transport-Security`: max-age=31536000 (force HTTPS)

## Testing

### Test frontend configuration loading:
1. Open browser DevTools
2. Go to Console tab
3. Type: `CONFIG.API_URL`
4. Should return your backend URL

### Test API connectivity:
```bash
curl https://your-domain.com/health
```

Should return:
```json
{"status": "healthy", "message": "Server is running"}
```

## Troubleshooting

### API requests failing (CORS errors)
1. Check that your domain is in `ALLOWED_ORIGINS` in `.env`
2. Ensure frontend is accessing from that exact domain (including http/https)
3. Restart Flask backend after changing `.env`

### Config.js not loading
1. Check browser DevTools Console for errors
2. Ensure `config.js` is in the `/Food incorporated/` folder
3. Verify all HTML files have `<script src="../config.js"></script>` in the `<head>`

### API calls to wrong URL
1. Check `CONFIG.API_URL` in browser console
2. Verify `API_HOST` and `API_PROTOCOL` in `.env`
3. Clear browser cache and reload

## Development vs Production

### Development Setup
```env
API_PROTOCOL=http
API_HOST=localhost
API_PORT=5000
```

### Production Setup
```env
API_PROTOCOL=https
API_HOST=s2330027.ncgrp.xyz
API_PORT=443
```

The `config.js` file automatically handles the http/https protocol based on where it's running.

## References

- Flask-CORS Documentation: https://flask-cors.readthedocs.io/
- Gunicorn: https://gunicorn.org/
- Nginx Reverse Proxy: https://nginx.org/
