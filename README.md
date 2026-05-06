# Food-Incorporated-Project

A full-stack web and desktop application for managing restaurant orders, menus, and kitchen operations.

## Project Structure

```
Food-Incorporated-Project/
├── Food incorporated/
│   ├── config.js                 # Domain configuration (NEW)
│   ├── Admin_Login/              # Admin login interface
│   │   ├── index.html
│   │   ├── script.js
│   │   └── style.css
│   ├── Menu/                     # Customer menu ordering interface
│   │   ├── menu.html
│   │   ├── menu.js
│   │   ├── menu.css
│   │   ├── checkout.html
│   │   └── checkout.js
│   ├── Images/                   # Product images
│   ├── Kitchen_app/              # Flask backend & desktop app
│   │   ├── server.py             # Flask API server
│   │   ├── app.py                # Desktop application (Tkinter)
│   │   ├── api.py                # Python API client
│   │   ├── models.py             # Database models
│   │   ├── requirements.txt      # Python dependencies
│   │   ├── .env                  # Configuration (UPDATE FOR YOUR DOMAIN)
│   │   └── widgets/              # Tkinter UI components
│   └── README.txt
├── DOMAIN_CONFIGURATION.md       # Domain setup guide (NEW)
├── CHANGES_SUMMARY.md            # Detailed change log (NEW)
└── README.md                     # This file
```

## Features

### Frontend (Customer)
- **Interactive Menu**: Browse food items with images and prices
- **Order Management**: Add/remove items, view total
- **Table Assignment**: Automatic table assignment system
- **Checkout**: Payment page with card validation

### Frontend (Admin)
- **Admin Login**: Secure login interface
- **Order Tracking**: View pending, preparing, and ready orders
- **Stock Management**: Track inventory levels with visual indicators

### Backend
- **Flask REST API**: Orders, tables, stock endpoints
- **Database**: SQLite/PostgreSQL support
- **CORS**: Configured for secure cross-origin requests
- **Security Headers**: HSTS, XSS protection, clickjacking prevention

### Desktop App (Kitchen)
- **Tkinter GUI**: Real-time order updates
- **Order Cards**: Visual status indicators
- **Stock Management**: Update inventory levels
- **Auto-refresh**: Real-time data synchronization

## Domain Configuration

**This project has been updated for domain-based deployment!**

### Quick Setup

1. **Update `.env` with your domain:**
   ```bash
   cd "Food incorporated/Kitchen_app"
   # Edit .env file:
   # API_HOST=your-domain.com
   # API_PROTOCOL=https
   # ALLOWED_ORIGINS=https://your-domain.com
   ```

2. **Frontend automatically adapts** - No hardcoded IPs needed!
   - JavaScript automatically detects your domain
   - API URLs constructed dynamically in `config.js`

3. **See [DOMAIN_CONFIGURATION.md](./DOMAIN_CONFIGURATION.md) for detailed setup**

### No More Hardcoded IPs!

Before: `http://51.132.179.154:5000` ❌  
After: Auto-configured for your domain ✅

**Key improvements:**
- ✅ Dynamic domain detection
- ✅ Environment-based configuration
- ✅ Production-ready security headers
- ✅ CORS properly configured
- ✅ Error handling with logging

## Installation

### Backend Setup

```bash
cd "Food incorporated/Kitchen_app"

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from server import init_db; init_db()"

# Run Flask server
python server.py
# Or with gunicorn: gunicorn server:app
```

### Desktop App Setup

```bash
cd "Food incorporated"

# Install dependencies
pip install -r Kitchen_app/requirements.txt

# Run desktop application
python Kitchen_app/app.py
```

### Frontend Setup

```bash
cd "Food incorporated"

# Option 1: Python built-in server (development)
python -m http.server 8000

# Option 2: Use with Nginx (production)
# See DOMAIN_CONFIGURATION.md for Nginx setup
```

Then open:
- Customer menu: `http://localhost:8000/Menu/menu.html`
- Admin login: `http://localhost:8000/Admin_Login/index.html`

## Environment Variables

Create `.env` in `Kitchen_app/` directory:

```env
# Domain Configuration
API_PROTOCOL=https              # http for dev, https for prod
API_HOST=your-domain.com        # Your actual domain
API_PORT=443                    # 443 for https, 5000 for dev

# CORS
ALLOWED_ORIGINS=https://your-domain.com,http://localhost:8000

# Database
DATABASE_URL=sqlite:///foodinc.db
# PostgreSQL: postgresql://user:password@host/dbname

# Security
FLASK_ENV=production
DEBUG=False
SECURE_HSTS_SECONDS=31536000
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Server health check |
| GET | `/orders` | Get all orders |
| POST | `/orders` | Create new order |
| PATCH | `/orders/<id>/status` | Update order status |
| GET | `/stock` | Get inventory |
| POST | `/stock/update` | Update stock quantity |
| GET | `/tables` | Get all tables |
| POST | `/tables/assign` | Assign table to customer |

## CORS Configuration

The backend is configured to accept requests only from specified origins. Update `ALLOWED_ORIGINS` in `.env`:

```env
ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com,http://localhost:8000
```

## Security Features

- **CORS**: Whitelist configured domains
- **HSTS**: Forces HTTPS in production
- **XSS Protection**: Multiple headers prevent attacks
- **Clickjacking Protection**: X-Frame-Options header
- **MIME Sniffing Prevention**: Content-Type header
- **Referrer Policy**: Control information leakage

## Deployment

### Development
```bash
# Terminal 1: Backend
cd "Food incorporated/Kitchen_app"
python server.py

# Terminal 2: Frontend
cd "Food incorporated"
python -m http.server 8000
```

### Production
See [DOMAIN_CONFIGURATION.md](./DOMAIN_CONFIGURATION.md) for:
- Nginx configuration
- SSL/HTTPS setup
- Gunicorn deployment
- Database migration
- Security hardening

## Technology Stack

### Frontend
- HTML5, CSS3, JavaScript (Vanilla)
- No frameworks (lightweight)
- Local storage for session data

### Backend
- **Flask**: Python web framework
- **Flask-CORS**: Cross-origin resource sharing
- **Flask-SQLAlchemy**: ORM for database
- **python-dotenv**: Environment configuration
- **Gunicorn**: WSGI HTTP Server
- **PostgreSQL/SQLite**: Database

### Desktop
- **Tkinter**: GUI framework
- **Requests**: HTTP client
- **Threading**: Async operations

## Database

### SQLite (Development)
Default, no setup needed. File: `foodinc.db`

### PostgreSQL (Production)
For production, update `DATABASE_URL` in `.env`:
```env
DATABASE_URL=postgresql://user:password@localhost/foodinc
```

Then run:
```bash
pip install psycopg2-binary
python -c "from server import init_db; init_db()"
```

## Troubleshooting

### API requests failing?
1. Check `CONFIG.API_URL` in browser console
2. Verify `.env` settings match your domain
3. Restart Flask server
4. See [DOMAIN_CONFIGURATION.md - Troubleshooting](./DOMAIN_CONFIGURATION.md#troubleshooting)

### CORS errors?
1. Add domain to `ALLOWED_ORIGINS` in `.env`
2. Use `http://` for development, `https://` for production
3. Restart Flask server

### Database errors?
1. Ensure `foodinc.db` file exists or run `init_db()`
2. Check database URL in `.env`
3. For PostgreSQL, verify connection details

## Recent Changes

✅ **May 2026**: Domain configuration system implemented
- Removed hardcoded IP addresses
- Dynamic API URL detection
- Environment-based configuration
- Added security headers
- See [CHANGES_SUMMARY.md](./CHANGES_SUMMARY.md) for details

## Project Status

- ✅ Core functionality working
- ✅ Domain configuration ready
- ✅ Security headers implemented
- ✅ CORS properly configured
- 🔄 Ready for production deployment

## Authors

School project team - Food Incorporated

## License

Internal use only
