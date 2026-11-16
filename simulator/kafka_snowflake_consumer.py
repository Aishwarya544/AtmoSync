
import os
import json
from datetime import datetime

from dotenv import load_dotenv
from kafka import KafkaConsumer
import snowflake.connector

# Load Snowflake credentials from the root .env file
load_dotenv()

# Connect to Snowflake
conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
    role=os.getenv("SNOWFLAKE_ROLE")
)

cursor = conn.cursor()

# Connect to Kafka
consumer = KafkaConsumer(
    "container-sensor-data",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda data: json.loads(data.decode("utf-8")),
    auto_offset_reset="latest",
    enable_auto_commit=True,
    group_id="atmosync-snowflake-consumer"
)

print("AtmoSync Snowflake Consumer Started!")
print("Waiting for sensor readings...")

try:
    for message in consumer:
        data = message.value

        recorded_at = datetime.fromisoformat(data["timestamp"])

        cursor.execute(
            """
            INSERT INTO ATMOSYNC_DB.RAW.SENSOR_READINGS
            (CONTAINER_ID, RECORDED_AT, TEMPERATURE_C,
             HUMIDITY_PERCENT, VIBRATION_G)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                data["container_id"],
                recorded_at,
                data["temperature_c"],
                data["humidity_percent"],
                data["vibration_g"]
            )
        )

        print("Saved to Snowflake:", data)

except KeyboardInterrupt:
    print("Consumer stopped.")

finally:
    consumer.close()
    cursor.close()
    conn.close()
    print("Snowflake connection closed.")
