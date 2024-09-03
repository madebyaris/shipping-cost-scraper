import os

# Default configuration (development)
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'shipping_costs_db'
}

API_KEYS = {
    'fastship': 'your_fastship_api_key'
}

# Check if production config exists and load it
if os.path.exists('config_production.py'):
    try:
        from config_production import MYSQL_CONFIG as PROD_MYSQL_CONFIG, API_KEYS as PROD_API_KEYS
        MYSQL_CONFIG.update(PROD_MYSQL_CONFIG)
        API_KEYS.update(PROD_API_KEYS)
        print("Loaded production configuration")
    except ImportError as e:
        print(f"Error loading production configuration: {e}")
else:
    print("Using default configuration")