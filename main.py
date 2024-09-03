import time
from db_handler import DatabaseHandler
from api_handlers.fastship_handler import FastShipHandler
from config import API_KEYS

def run_scraper():
    db = DatabaseHandler()
    fastship_handler = FastShipHandler(API_KEYS['fastship'])

    try:
        # Fetch origins and destinations from the database
        origins = fetch_locations(db, ['city', 'regency'])
        destinations = fetch_locations(db, ['city', 'regency'])

        for origin in origins:
            for destination in destinations:
                # Skip if origin and destination are the same
                if origin['id'] == destination['id']:
                    continue

                # Example weight in kg
                weight = 1

                shipping_costs = fastship_handler.get_shipping_cost(
                    f"{origin['name']}, {origin['type']}",
                    f"{destination['name']}, {destination['type']}",
                    weight
                )

                if shipping_costs:
                    save_shipping_costs(db, origin['id'], destination['id'], 'FastShip', shipping_costs)

                # Add a small delay to avoid overwhelming the API
                time.sleep(1)

    finally:
        fastship_handler.close_session()
        db.close_connection()

def fetch_locations(db, types):
    cursor = db.connection.cursor(dictionary=True)
    try:
        type_placeholders = ', '.join(['%s'] * len(types))
        cursor.execute(f"""
            SELECT id, name, type, parent_id
            FROM origins
            WHERE type IN ({type_placeholders})
        """, types)
        return cursor.fetchall()
    finally:
        cursor.close()

def save_shipping_costs(db, origin_id, destination_id, expedition, shipping_costs):
    cursor = db.connection.cursor()
    try:
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