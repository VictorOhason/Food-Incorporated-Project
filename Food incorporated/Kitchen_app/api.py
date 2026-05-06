import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API URL from environment, with sensible defaults
API_PROTOCOL = os.getenv('API_PROTOCOL', 'http')
API_HOST = os.getenv('API_HOST', 'localhost')
API_PORT = os.getenv('API_PORT', '5000')
BASE_URL = f"{API_PROTOCOL}://{API_HOST}:{API_PORT}"

def fetch_orders():
    """Fetch all orders from the server."""
    try:
        response = requests.get(f"{BASE_URL}/orders")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching orders from {BASE_URL}/orders: {e}")
        raise

def update_order_status(order_id, status):
    """Update the status of an order."""
    try:
        payload = {"status": status}
        response = requests.patch(f"{BASE_URL}/orders/{order_id}/status", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error updating order status: {e}")
        raise

def fetch_stock():
    """Fetch current stock levels from the server."""
    try:
        response = requests.get(f"{BASE_URL}/stock")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching stock from {BASE_URL}/stock: {e}")
        raise

def update_stock(item_id, change):
    """Update stock quantity for an item."""
    try:
        payload = {"id": item_id, "change": change}
        response = requests.post(f"{BASE_URL}/stock/update", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error updating stock: {e}")
        raise