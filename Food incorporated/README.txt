Food Incorporated - Project Overview

This document explains the purpose of each major file in the workspace and how the application works.

---

1) Project Structure

config.js          - auto-detects server domain/IP for frontend API calls; dynamically constructs API URLs.

Admin_Login/
  index.html       - login page for customers/staff.
  script.js        - email-only login flow, saves customer name/email to localStorage, and redirects to menu.
  style.css        - visual styling for the login page.

Images/
  (image files)    - asset folder containing food images used by the menu carousel.

Menu/
  menu.html        - customer menu page used to select items and place orders; loads config.js first.
  menu.js          - frontend menu behavior: table assignment, carousel, item quantity, order summary, order submission.
  menu.css         - styling for menu page.
  checkout.html    - order review/checkout page for finalizing orders; loads config.js first.
  checkout.js      - frontend checkout behavior for order submission.

Kitchen_app/
  server.py        - Flask REST API backend; handles orders, stock, tables, table assignment.
  models.py        - SQLAlchemy database models: stores, tables, stock, orders.
  api.py           - Python API client for desktop/kitchen app to connect to Flask backend.
  app.py           - Desktop application (Tkinter) for kitchen staff.
  requirements.txt - Python dependency list for backend runtime.
  .env             - configuration file: database, API settings, CORS, security.
  widgets/         - Tkinter UI components for desktop app.

create_favicon.py  - script to generate the favicon file.

---

2) How It Works

Frontend (Menu & Checkout):
  1. User opens menu.html or checkout.html
  2. Browser loads config.js which auto-detects the server IP/domain
  3. JavaScript uses CONFIG object with dynamically-constructed API URLs
  4. API calls are sent to http://[server-ip]:5000 or https://[domain]:443
  5. config.js handles localhost, IP addresses, and domain names automatically

Backend (Flask server.py):
  1. Reads configuration from .env file (API settings, database, CORS, security)
  2. Initializes SQLite database (foodinc.db) with sample data on first run
  3. Listens on port 5000, accepts requests from allowed origins (CORS)
  4. Provides REST API endpoints for orders, stock, and table management
  5. Runs background cleanup every 60 seconds to free tables after 30 minutes

Python API Client (api.py):
  1. Used by desktop app (app.py) and kitchen staff interface
  2. Reads API settings from .env (protocol, host, port)
  3. Connects to Flask backend using environment variables for flexibility
  4. Allows kitchen staff to manage orders and inventory from desktop application

---

3) Key Features

- Dynamic URL Detection: No hardcoded IPs in code; config.js handles any domain/IP
- Environment Configuration: .env file controls all settings (database, CORS, API)
- Database: SQLite by default (automatic setup), PostgreSQL/MySQL optional
- Security: CORS headers, X-Frame-Options, Content-Type protection, HSTS
- Automatic Database Initialization: Tables created automatically on first run
- Multi-Store Support: Each store has 10 tables with automatic state management

---

4) Backend API Endpoints

GET /health                       - health check
GET /orders                       - all orders
POST /orders                      - create new order
PATCH /orders/<order_id>/status   - update order status
GET /stock                        - kitchen inventory
POST /stock/update                - update stock quantity
GET /tables                       - all tables, all stores
GET /tables/<store_id>            - tables for one store
POST /tables/assign               - reserve next free table
PATCH /tables/<store_id>/<table_id>/free - free a table

---

5) Configuration

Environment Variables (.env):
  DATABASE_URL      - database connection (default: sqlite:///foodinc.db)
  API_PROTOCOL      - http or https (default: https for production)
  API_HOST          - server domain/IP (default: s2330027.ncgrp.xyz)
  API_PORT          - API port (default: 443 for https, 5000 for dev)
  ALLOWED_ORIGINS   - CORS allowed domains (default: current domain + localhost:8000)
  FLASK_ENV         - production or development
  DEBUG             - True/False for Flask debug mode
  PORT              - frontend server port (default: 5000 for API)

---

6) Deployment

Development:
  Terminal 1: cd "Food incorporated/Kitchen_app" && python server.py
  Terminal 2: cd "Food incorporated" && python -m http.server 8000
  Access: http://localhost:8000/Menu/menu.html

Production (School Server):
  1. Copy "Food incorporated" folder to server
  2. pip install -r Kitchen_app/requirements.txt
  3. Update .env with domain and CORS settings
  4. python Kitchen_app/server.py
  5. Serve frontend files on port 8000
  6. Access via browser: http://[server-ip]:8000/Menu/menu.html
  * Database not seeded because `init_db()` was not run or the database file is not writable.
  * Order stock decrement logic may not match names exactly, creating inconsistent inventory updates.
  * Duplicate `orderNumber` values can fail if an order with the same number already exists.

---

3) Backend Models: Kitchen_app/models.py

Purpose: Defines the persistent data schema for the backend.

Models:

- Store
  * `store_id`: external store identifier, e.g. `store1`.
  * `name` and `location`
  * Relationships to `Table` and `Order`.

- Table
  * `table_id`: table number inside a store.
  * `status`: `free` or `occupied`.
  * `assigned_to`: email of the customer currently using the table.
  * `occupied_since`: timestamp when the table was assigned.
  * Unique constraint on `(store_id, table_id)`.

- StockItem
  * `name`, `quantity`, `unit`
  * Used by the kitchen inventory API.

- Order
  * `order_number`: unique order id used by application flow.
  * `table_number`, `customer_name`, `customer_email`
  * `status`: order lifecycle state.
  * `items`: JSON payload of the ordered items.
  * `total`: order total amount.

Each model includes `to_dict()` for JSON serialization.

Common model issues:
  * If the `store_id` or `table_id` fields are inconsistent between frontend and backend, table assignment will fail.
  * `items` stored as JSON must be valid JSON; invalid payloads may break order creation.
  * `order_number` collisions can prevent new orders from being saved.

---

4) Frontend: Admin_Login/script.js

Purpose: simple login experience using email only.

Key behavior:
  * Validates that an email is present and in the correct format.
  * Stores `customerName` and `customerEmail` in localStorage.
  * Redirects to `../Menu/menu.html` after login.
  * Includes a placeholder social login button with a future stub.

Common issues:
  * localStorage blocked by browser privacy settings causes sign-in failure.
  * Missing or incorrect path to `../Menu/menu.html` prevents redirect.
  * Invalid email entry triggers validation alerts.

---

5) Frontend: Menu/menu.js

Purpose: handles table assignment, menu interactions, order summary, and order submission.

Key functions and areas:

- Global configuration
  * `ASSIGNED_TABLE` / `ASSIGNED_STORE`
  * `LIVE_SERVER_URL` and `TABLE_API_URL` point to backend endpoints.

- `window.onload`
  * Checks `sessionStorage` for a cached table assignment.
  * If none exists, calls `assignTableFromServer()`.
  * Restores the saved customer name in the menu form.
  * Starts the image carousel.
  * Adds aria labels to quantity buttons.

- `assignTableFromServer()`
  * Posts to `/tables/assign` and stores the result in sessionStorage.
  * Falls back to a random table if assignment fails.

- `displayTable()`
  * Updates the UI with the current assigned table.

- `startCarousel()`
  * Rotates food images every 5 seconds.
  * Updates alt text and announcements for accessibility.

- Quantity button handling
  * Increases or decreases item quantities.
  * Changes quantity styling when item count is above zero.

- Form submit handling
  * Builds an order summary from selected items.
  * Performs validation to ensure at least one item is selected.
  * Generates a random `orderNumber` and stores order details in `currentOrder`.
  * Opens a modal for confirmation.

- Modal accessibility
  * `openModal()` and `closeModal()` manage focus and visibility.
  * Escape closes the modal.
  * Tab key focus is trapped inside the modal.

Common frontend issues:
  * If the server is not running, `/tables/assign` will fail and the page uses a fallback table.
  * Cross-origin issues when backend and frontend are served from different hosts.
  * Missing DOM elements in HTML can break menu.js if selectors return null.
  * The frontend uses `sessionStorage` for table state and `localStorage` for identity, so browser storage must be enabled.
  * `orderNumber` is generated randomly by the frontend and may collide with existing backend records.

---

6) General Application Flow

1. User opens `Admin_Login/index.html`.
2. They enter an email and submit the form.
3. `script.js` stores the user email and name locally.
4. The browser redirects to `Menu/menu.html`.
5. `menu.js` assigns or restores a table from the backend.
6. The user selects menu items and submits the order.
7. The frontend sends the order payload to `Kitchen_app/server.py` via `/orders`.
8. The backend saves the order, updates stock, and stores table assignment state.
9. The background thread periodically frees tables held longer than 30 minutes.

---

7) Deployment and Environment Notes

- Use `.env` in `Kitchen_app` to define:
  * `DATABASE_URL` for the SQLAlchemy database.
  * `PORT` for the Flask server.
  * `DEBUG` to enable debug mode.
  * `ALLOWED_ORIGINS` for CORS origin control.

- Default database is SQLite at `sqlite:///foodinc.db`.
- For PostgreSQL, set `DATABASE_URL=postgresql://user:pass@host:port/dbname`.
- Ensure the backend is launched from `Kitchen_app` if relative imports are used.

Common deployment issues:
  * `postgres://` URIs must be converted to `postgresql://`.
  * `ALLOWED_ORIGINS` must include the frontend origin or else CORS blocks requests.
  * If the app starts without `init_db()`, the tables may not exist.
  * Running backend from the wrong working directory can break relative imports.

---

8) Notes on Legacy/Unused Files

- `Kitchen_app/qt6-old-app.txt` is a legacy PyQt draft and not used by the current web-based menu/order system.
- `create_favicon.py` is a utility script for the favicon and is not part of regular runtime.
- `Tutorial for FoodInc.mp4` is a demo/tutorial asset and does not affect application logic.

---

Use this file as a quick reference for how the app is organized, which backend routes support each feature, and what to verify when the system does not behave as expected.
