# Food-Incorporated-Project

A full-stack web and desktop application for managing restaurant orders, menus, and kitchen operations.

## Project Structure

```
Food-Incorporated-Project/
├── Food incorporated/
│   ├── config.js                 # Auto-detects server domain/IP
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
│   │   ├── .env                  # Configuration
│   │   └── widgets/              # Tkinter UI components
│   └── README.txt
└── README.md
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

## Automatic Domain Detection

The frontend automatically detects your server's domain or IP address. No hardcoded IPs needed.

How it works:
- config.js detects hostname from window.location
- Automatically constructs API URLs for any domain/IP
- Works on localhost, school servers, or any deployment
- Frontend calls backend at http://[current-server]:5000

Configuration:
- Edit Kitchen_app/.env to customize API settings
- ALLOWED_ORIGINS controls which servers can access the API
- Default works for all origins (good for school networks)

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

# Start Python file server (development)
python -m http.server 8000
```

Then open:
- Customer menu: http://localhost:8000/Menu/menu.html
- Admin login: http://localhost:8000/Admin_Login/index.html

From another computer:
- Replace localhost with your server IP address

## Environment Variables

Configuration is in Kitchen_app/.env:

```env
# Database
DATABASE_URL=sqlite:///foodinc.db

# API Server Configuration
API_PROTOCOL=https
API_HOST=s2330027.ncgrp.xyz
API_PORT=443

# CORS - allowed origins
ALLOWED_ORIGINS=https://s2330027.ncgrp.xyz,http://localhost:8000

# Server
FLASK_ENV=production
DEBUG=False
PORT=5000
```

For development on localhost, adjust:
```env
API_PROTOCOL=http
API_HOST=localhost
API_PORT=5000
ALLOWED_ORIGINS=http://localhost:8000
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

### Development (Local)
```bash
# Terminal 1: Backend API
cd "Food incorporated/Kitchen_app"
python server.py

# Terminal 2: Frontend server
cd "Food incorporated"
python -m http.server 8000
```

Access at: http://localhost:8000/Menu/menu.html

### Production (School Server)
1. Copy "Food incorporated" folder to server
2. Install: pip install -r Kitchen_app/requirements.txt
3. Update .env with your server details
4. Run: python Kitchen_app/server.py
5. Serve frontend files on port 8000

Frontend auto-detects your server IP/domain

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
1. Check `CONFIG.API_URL` in browser console (F12)
2. Verify .env settings match your server
3. Make sure Flask server is running on port 5000
4. Check port 5000 is not blocked by firewall

### CORS errors?
1. Add domain/IP to ALLOWED_ORIGINS in .env
2. Restart Flask server after changing .env
3. Check protocol (http vs https) matches

### Database errors?
1. Delete foodinc.db to reset
2. Restart Flask server to recreate database
3. Check write permissions in Kitchen_app/ folder

## Authors

School project team - Food Incorporated

## License

Internal use only
