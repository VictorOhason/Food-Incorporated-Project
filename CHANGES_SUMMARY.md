# Domain Configuration - Changes Summary

## Files Created

### 1. `/Food incorporated/config.js` (NEW)
- Automatically detects current domain from `window.location`
- Constructs API URLs dynamically based on environment (development vs production)
- Provides global `CONFIG` object with API endpoints
- Supports both localhost and production domains

**Key features:**
- Protocol detection (http vs https)
- Hostname detection
- Fallback mechanism for API URLs
- Helper methods for endpoint construction

---

## Files Modified

### 1. `/Food incorporated/Kitchen_app/api.py`
**Changes:**
- Removed hardcoded IP: `http://51.132.179.154:5000`
- Added environment variable support:
  - `API_PROTOCOL` (default: http)
  - `API_HOST` (default: localhost)
  - `API_PORT` (default: 5000)
- Added error handling with informative messages
- Updated all functions with try-catch and proper error logging

**Before:**
```python
BASE_URL = "http://51.132.179.154:5000"
```

**After:**
```python
API_PROTOCOL = os.getenv('API_PROTOCOL', 'http')
API_HOST = os.getenv('API_HOST', 'localhost')
API_PORT = os.getenv('API_PORT', '5000')
BASE_URL = f"{API_PROTOCOL}://{API_HOST}:{API_PORT}"
```

---

### 2. `/Food incorporated/Menu/menu.js`
**Changes:**
- Removed hardcoded IPs:
  - `http://51.132.179.154:5000/orders`
  - `http://51.132.179.154:5000/tables`
- Added dynamic API URL resolution from `config.js`
- Added fallback mechanism if CONFIG object not available
- URLs now constructed from `CONFIG.ORDERS_URL` and `CONFIG.TABLES_URL`

**Before:**
```javascript
const LIVE_SERVER_URL = "http://51.132.179.154:5000/orders";
const TABLE_API_URL = "http://51.132.179.154:5000/tables";
```

**After:**
```javascript
const getApiUrl = () => {
    if (typeof CONFIG !== 'undefined') {
        return CONFIG.ORDERS_URL;
    }
    const protocol = window.location.protocol;
    const hostname = window.location.hostname;
    return `${protocol}//${hostname}/orders`;
};
```

---

### 3. `/Food incorporated/Menu/menu.html`
**Changes:**
- Added `<script src="../config.js"></script>` in `<head>` section
- Ensures configuration is loaded before menu.js runs
- Maintains load order: config.js → menu.js

---

### 4. `/Food incorporated/Menu/checkout.html`
**Changes:**
- Added `<script src="../config.js"></script>` in `<head>` section
- Ensures configuration is loaded before checkout.js runs

---

### 5. `/Food incorporated/Kitchen_app/.env`
**Changes:**
- Updated ALLOWED_ORIGINS to include domain: `s2330027.ncgrp.xyz`
- Added API configuration variables:
  - `API_PROTOCOL=https`
  - `API_HOST=s2330027.ncgrp.xyz`
  - `API_PORT=443`
- Added security headers configuration:
  - `SECURE_HSTS_SECONDS=31536000`
  - `SECURE_HSTS_INCLUDE_SUBDOMAINS=True`
- Added server configuration:
  - `FLASK_ENV=production`
  - `DEBUG=False`

---

### 6. `/Food incorporated/Kitchen_app/server.py`
**Changes:**
- Added whitespace stripping for ALLOWED_ORIGINS parsing
- Added security headers decorator (`@app.after_request`)
- Implements multiple security headers:
  - X-Frame-Options (prevent clickjacking)
  - X-Content-Type-Options (prevent MIME sniffing)
  - X-XSS-Protection (enable XSS protection)
  - Referrer-Policy (control referrer sharing)
  - Permissions-Policy (restrict API access)
  - Strict-Transport-Security (HSTS for HTTPS)

---

## Documentation Created

### 1. `/DOMAIN_CONFIGURATION.md` (NEW)
Comprehensive guide covering:
- Overview of the configuration system
- Frontend configuration details
- Backend configuration details
- Step-by-step deployment instructions
- CORS configuration
- Security headers explanation
- Testing procedures
- Troubleshooting guide
- Development vs Production setup

---

## Technical Details

### Configuration System Flow

```
┌─────────────────────────────────────────┐
│         Browser accesses domain         │
│    (e.g., https://example.com)          │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   HTML loads config.js                  │
│  (reads window.location)                │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  CONFIG object available globally       │
│  CONFIG.API_URL = correct domain        │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  menu.js / other scripts load           │
│  Use CONFIG.ORDERS_URL, etc.            │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   API requests to correct domain        │
│   (no more hardcoded IPs!)              │
└─────────────────────────────────────────┘
```

### Backend Configuration Flow

```
┌──────────────────────────────┐
│   .env file                  │
│ (API_HOST, API_PROTOCOL)     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│   api.py loads environment   │
│   Constructs BASE_URL        │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│   Python clients use         │
│   BASE_URL for requests      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│   Server responds with       │
│   security headers           │
└──────────────────────────────┘
```

---

## Security Improvements

1. **CORS Configuration**: Only allows specified origins
2. **Security Headers**: Multiple headers prevent common attacks
3. **HSTS**: Forces HTTPS in production
4. **Error Handling**: Better error messages without exposing sensitive info
5. **Environment-based**: Secrets not hardcoded in files

---

## Testing Checklist

- [ ] Open `https://your-domain.com` in browser
- [ ] Open DevTools Console
- [ ] Type: `CONFIG.API_URL`
- [ ] Should return: `https://your-domain.com` (or your domain)
- [ ] Check Network tab - API requests should go to correct domain
- [ ] Test order submission
- [ ] Test kitchen app connecting to API
- [ ] Verify CORS errors are gone

---

## Next Steps for Deployment

1. **Update `.env`** with your actual domain:
   ```bash
   API_HOST=your-actual-domain.com
   ALLOWED_ORIGINS=https://your-actual-domain.com
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize database**:
   ```bash
   python -c "from server import init_db; init_db()"
   ```

4. **Set up reverse proxy** (Nginx/Apache) to serve both frontend and backend

5. **Configure SSL/HTTPS** with valid certificates

6. **Test all endpoints** to ensure they're working

---

## Rollback Information

If needed, all changes are reversible:
- Remove `config.js` script tags from HTML
- Revert to hardcoded URLs in menu.js and api.py
- Use old `.env` configuration

However, the new configuration system is recommended for maintainability.
