import requests
from db_handler import DatabaseHandler

BASE_URL = "http://www.emsifa.com/api-wilayah-indonesia/api"

def fetch_data(endpoint):
    response = requests.get(f"{BASE_URL}/{endpoint}")
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

def insert_initial_data():
    db = DatabaseHandler()
    cursor = db.connection.cursor()

    try:
        # Insert provinces
        provinces = fetch_data("provinces.json")
        for province in provinces:
            cursor.execute("""
                INSERT INTO origins (id, name, type, parent_id)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                name = VALUES(name), type = VALUES(type), parent_id = VALUES(parent_id)
            """, (province['id'], province['name'], 'province', None))
            
            # Insert regencies
            regencies = fetch_data(f"regencies/{province['id']}.json")
            for regency in regencies:
                cursor.execute("""
                    INSERT INTO origins (id, name, type, parent_id)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    name = VALUES(name), type = VALUES(type), parent_id = VALUES(parent_id)
                """, (regency['id'], regency['name'], 'regency' if 'KABUPATEN' in regency['name'] else 'city', province['id']))
                
                # Insert districts
                districts = fetch_data(f"districts/{regency['id']}.json")
                for district in districts:
                    cursor.execute("""
                        INSERT INTO origins (id, name, type, parent_id)
                        VALUES (%s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                        name = VALUES(name), type = VALUES(type), parent_id = VALUES(parent_id)
                    """, (district['id'], district['name'], 'district', regency['id']))
                    
                    # Insert villages
                    villages = fetch_data(f"villages/{district['id']}.json")
                    for village in villages:
                        cursor.execute("""
                            INSERT INTO origins (id, name, type, parent_id)
                            VALUES (%s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE
                            name = VALUES(name), type = VALUES(type), parent_id = VALUES(parent_id)
                        """, (village['id'], village['name'], 'village', district['id']))

        db.connection.commit()
        print("Initial data inserted successfully")
    except Exception as e:
        print(f"Error inserting initial data: {e}")
        db.connection.rollback()
    finally:
        cursor.close()
        db.close_connection()

if __name__ == "__main__":
    insert_initial_data()