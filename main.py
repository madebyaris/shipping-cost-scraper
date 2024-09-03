import time
from db_handler import DatabaseHandler
from api_handlers.fastship_handler import FastShipHandler
from config import API_KEYS

def run_scraper():
    db = DatabaseHandler()
    fastship_handler = FastShipHandler(API_KEYS['fastship'])

    # Example origins and destinations
    origins = [
        {'name': 'DKI Jakarta', 'type': 'province', 'parent_id': None},
        {'name': 'Jakarta', 'type': 'city', 'parent_id': 1},
        {'name': 'East Java', 'type': 'province', 'parent_id': None},
        {'name': 'Surabaya', 'type': 'city', 'parent_id': 3},
    ]
    
    destinations = [
        {'name': 'West Java', 'type': 'province', 'parent_id': None},
        {'name': 'Bandung', 'type': 'city', 'parent_id': 5},
        {'name': 'North Sumatra', 'type': 'province', 'parent_id': None},
        {'name': 'Medan', 'type': 'city', 'parent_id': 7},
    ]

    try:
        for origin in origins:
            for destination in destinations:
                # Skip if origin and destination are the same
                if origin['name'] == destination['name']:
                    continue

                # Example weight in kg
                weight = 1

                shipping_costs = fastship_handler.get_shipping_cost(
                    f"{origin['name']}, {origin['type']}",
                    f"{destination['name']}, {destination['type']}",
                    weight
                )

                if shipping_costs:
                    save_shipping_costs(db, origin, destination, 'FastShip', shipping_costs)

                # Add a small delay to avoid overwhelming the API
                time.sleep(1)

    finally:
        fastship_handler.close_session()
        db.close_connection()

def save_shipping_costs(db, origin, destination, expedition, shipping_costs):
    cursor = db.connection.cursor()
    try:
        # Insert or get origin
        cursor.execute(
            "INSERT IGNORE INTO origins (name, type, parent_id) VALUES (%s, %s, %s)",
            (origin['name'], origin['type'], origin['parent_id'])
        )
        cursor.execute(
            "SELECT id FROM origins WHERE name = %s AND type = %s",
            (origin['name'], origin['type'])
        )
        origin_id = cursor.fetchone()[0]

        # Insert or get destination
        cursor.execute(
            "INSERT IGNORE INTO origins (name, type, parent_id) VALUES (%s, %s, %s)",
            (destination['name'], destination['type'], destination['parent_id'])
        )
        cursor.execute(
            "SELECT id FROM origins WHERE name = %s AND type = %s",
            (destination['name'], destination['type'])
        )
        destination_id = cursor.fetchone()[0]

        # Insert or get expedition
        cursor.execute(
            "INSERT IGNORE INTO expeditions (name) VALUES (%s)",
            (expedition,)
        )
        cursor.execute("SELECT id FROM expeditions WHERE name = %s", (expedition,))
        expedition_id = cursor.fetchone()[0]

        # Insert or get shipping route
        cursor.execute("""
            INSERT IGNORE INTO shipping_routes (origin_id, destination_id)
            VALUES (%s, %s)
        """, (origin_id, destination_id))
        cursor.execute(
            "SELECT id FROM shipping_routes WHERE origin_id = %s AND destination_id = %s",
            (origin_id, destination_id)
        )
        route_id = cursor.fetchone()[0]

        # Insert shipping costs
        for cost_data in shipping_costs:
            cursor.execute("""
                INSERT INTO shipping_costs 
                (route_id, expedition_id, service, cost, estimated_days)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                cost = VALUES(cost), estimated_days = VALUES(estimated_days)
            """, (
                route_id,
                expedition_id,
                cost_data['service'],
                cost_data['cost'],
                cost_data['estimated_days']
            ))

        db.connection.commit()
    except Exception as e:
        print(f"Error saving shipping costs: {e}")
        db.connection.rollback()
    finally:
        cursor.close()

if __name__ == "__main__":
    run_scraper()