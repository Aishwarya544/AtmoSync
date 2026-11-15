
import json
import os
import psycopg2
from kafka import KafkaConsumer

# Connect to PostgreSQL
db_password = os.getenv("DB_PASSWORD")

if not db_password:
    raise ValueError("Please set the DB_PASSWORD environment variable.")

conn = psycopg2.connect(
    host="localhost",
    database="atmosync_db",
    user="postgres",
    password=db_password,
    port="5432"
)

cursor = conn.cursor()

# Connect to Kafka
consumer = KafkaConsumer(
    "container-sensor-data",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda data: json.loads(data.decode("utf-8")),
    auto_offset_reset="latest",
    enable_auto_commit=True,
    group_id="atmosync-postgres-consumer"
)

print("AtmoSync Kafka Consumer Started!")
print("Waiting for sensor readings...")

try:
    for message in consumer:
        data = message.value

        cursor.execute(
            """
            INSERT INTO sensor_readings
            (container_id, recorded_at, temperature_c,
             humidity_percent, vibration_g)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                data["container_id"],
                data["timestamp"],
                data["temperature_c"],
                data["humidity_percent"],
                data["vibration_g"]
            )
        )

        conn.commit()
        print("Saved to PostgreSQL:", data)

except KeyboardInterrupt:
    print("Consumer stopped.")

finally:
    consumer.close()
    cursor.close()
    conn.close()
