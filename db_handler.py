import mysql.connector
from mysql.connector import Error
from config import MYSQL_CONFIG

class DatabaseHandler:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**MYSQL_CONFIG)
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")

    def create_tables(self):
        cursor = self.connection.cursor()
        try:
            # Create origins table (unchanged)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS origins (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    type ENUM('province', 'city', 'regency') NOT NULL,
                    parent_id INT,
                    FOREIGN KEY (parent_id) REFERENCES origins(id)
                )
            """)

            # Create expeditions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS expeditions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(50) NOT NULL UNIQUE
                )
            """)

            # Create shipping_routes table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS shipping_routes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    origin_id INT,
                    destination_id INT,
                    FOREIGN KEY (origin_id) REFERENCES origins(id),
                    FOREIGN KEY (destination_id) REFERENCES origins(id),
                    UNIQUE KEY (origin_id, destination_id)
                )
            """)

            # Create shipping_costs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS shipping_costs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    route_id INT,
                    expedition_id INT,
                    service VARCHAR(50) NOT NULL,
                    cost DECIMAL(10, 2) NOT NULL,
                    estimated_days INT,
                    FOREIGN KEY (route_id) REFERENCES shipping_routes(id),
                    FOREIGN KEY (expedition_id) REFERENCES expeditions(id),
                    UNIQUE KEY (route_id, expedition_id, service)
                )
            """)

            self.connection.commit()
            print("Tables created successfully")
        except Error as e:
            print(f"Error creating tables: {e}")
        finally:
            cursor.close()

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")

# Usage example
if __name__ == "__main__":
    db = DatabaseHandler()
    db.create_tables()
    db.close_connection()