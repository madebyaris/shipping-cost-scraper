# Shipping Cost Scraper

This project is a Python-based scraper that collects shipping cost data from multiple expedition APIs in Indonesia. It stores the data in a MySQL database for easy access and analysis.

## Prerequisites

- Python 3.7+
- MySQL Server
- pip (Python package manager)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/madebyaris/shipping-cost-scraper.git
   cd shipping-cost-scraper
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install mysql-connector-python requests flask
   ```

4. Set up your MySQL database:
   - Create a new database named `shipping_costs_db`
   - Update the `config.py` file with your MySQL credentials and API keys

## Configuration

The project uses a configuration file `config.py` for setting up MySQL connection and API keys. For production environments, you can create a `config_production.py` file with production-specific settings.

1. For development, edit the `config.py` file directly:

   ```python
   MYSQL_CONFIG = {
       'host': 'localhost',
       'user': 'your_username',
       'password': 'your_password',
       'database': 'shipping_costs_db'
   }

   API_KEYS = {
       'fastship': 'your_fastship_api_key'
   }
   ```

2. For production, create a `config_production.py` file with the same structure:

   ```python
   MYSQL_CONFIG = {
       'host': 'production_host',
       'user': 'production_username',
       'password': 'production_password',
       'database': 'production_database'
   }

   API_KEYS = {
       'fastship': 'production_fastship_api_key'
   }
   ```

   The `config.py` file will automatically use these production settings if `config_production.py` exists.

Note: Make sure to add `config_production.py` to your `.gitignore` file to keep sensitive production data out of version control.

## Usage

1. First, run the database setup script to create the necessary tables:
   ```
   python db_handler.py
   ```

2. To start the scraper, run:
   ```
   python main.py
   ```

The scraper will collect shipping cost data for the predefined origins and destinations using the FastShip API. The data will be stored in the MySQL database.

## Using the HTTP API

The project includes a simple HTTP API for retrieving shipping cost data. To use it:

1. Start the API server:
   ```
   python api_server.py
   ```

2. The API will be available at `http://localhost:5000`. You can use the following endpoint:

   - GET `/shipping_cost`
     
     Parameters:
     - `origin`: Name of the origin city
     - `destination`: Name of the destination city
     - `weight`: Weight of the package in kg

   Example request:
   ```
   http://localhost:5000/shipping_cost?origin=Jakarta&destination=Surabaya&weight=1
   ```

   The API will return a JSON response with the available shipping options and their costs.

3. You can test the API using curl or any HTTP client:
   ```
   curl "http://localhost:5000/shipping_cost?origin=Jakarta&destination=Surabaya&weight=1"
   ```

## Project Structure

- `main.py`: The main script that runs the scraper
- `db_handler.py`: Handles database connections and table creation
- `config.py`: Contains configuration for MySQL and API keys
- `api_handlers/base_handler.py`: Base class for API handlers
- `api_handlers/fastship_handler.py`: Specific handler for FastShip API (contoh dari luar)
- `api_server.py`: HTTP API server for retrieving shipping cost data

## Extending the Scraper

To add support for additional shipping companies:

1. Create a new handler in the `api_handlers` directory, inheriting from `BaseAPIHandler`
2. Implement the `get_shipping_cost` and `parse_response` methods
3. Update `main.py` to use the new handler

## Troubleshooting

- If you encounter database connection issues, make sure your MySQL server is running and the credentials in `config.py` are correct.
- For API-related errors, check that your API keys are valid and properly set in `config.py`.
- If the HTTP API is not responding, ensure that the Flask server is running and there are no port conflicts.

## Initializing Data

After setting up the database, you can insert initial data for all Indonesian provinces, cities, regencies, districts, and villages:

1. Ensure you have the `requests` library installed:
   ```
   pip install requests
   ```

2. Run the data initialization script:
   ```
   python insert_initial_data.py
   ```

This script will:
- Fetch up-to-date data from the emsifa API
- Populate the `origins` table with a complete set of administrative divisions in Indonesia, including:
  - Provinces
  - Cities
  - Regencies (Kabupaten)
  - Districts (Kecamatan)
  - Villages (Desa/Kelurahan)

The data is structured hierarchically, with each entry having a `parent_id` that references its parent division.

Note: This process may take several minutes due to the large amount of data being inserted.

If you encounter any issues related to packet size, you may need to increase the `max_allowed_packet` size in your MySQL configuration. Contact your database administrator or refer to MySQL documentation for guidance on this setting.

## License

Private Lisensi buat Aris dan Tiyo