 
import random
import time
from datetime import datetime

import psycopg2


# PostgreSQL database connection
def connect_to_db():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="atmosync_db",
            user="postgres",
            password="aishu509",
            port="5432"
        )
        print("Connected to PostgreSQL successfully!")
        return connection

    except psycopg2.Error as error:
        print("Database connection failed:", error)
        return None


# Generate simulated IoT sensor data
def generate_sensor_reading():
    return {
        "container_id": "CONTAINER_001",
        "recorded_at": datetime.now(),
        "temperature_c": round(random.uniform(15, 35), 2),
        "humidity_percent": round(random.uniform(40, 90), 2),
        "vibration_g": round(random.uniform(0.10, 1.00), 2)
    }


# Store sensor data in PostgreSQL
def save_sensor_reading(connection, reading):
    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO sensor_readings
            (container_id, recorded_at, temperature_c,
             humidity_percent, vibration_g)
            VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            reading["container_id"],
            reading["recorded_at"],
            reading["temperature_c"],
            reading["humidity_percent"],
            reading["vibration_g"]
        )

        cursor.execute(query, values)
        connection.commit()
        cursor.close()

        print("Sensor reading saved:", reading)

    except psycopg2.Error as error:
        connection.rollback()
        print("Error saving sensor data:", error)


# Main program
def main():
    connection = connect_to_db()

    if connection is None:
        return

    try:
        while True:
            reading = generate_sensor_reading()
            save_sensor_reading(connection, reading)
            time.sleep(5)

    except KeyboardInterrupt:
        print("\nSensor simulation stopped.")

    finally:
        connection.close()
        print("Database connection closed.")


if __name__ == "__main__":
    main()
