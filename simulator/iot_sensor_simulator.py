
import random
import time
import json
import csv
from datetime import datetime
from pathlib import Path
from kafka import KafkaProducer

# ---------------------------------
# AtmoSync Project Configuration
# ---------------------------------

project_folder = Path(__file__).resolve().parent.parent

output_file = (
    project_folder / "data" / "raw" / "sensor_readings.csv"
)

kafka_topic = "container-sensor-data"
kafka_server = "localhost:9092"

# ---------------------------------
# Connect to Kafka
# ---------------------------------

print("Connecting to Kafka...")

producer = KafkaProducer(
    bootstrap_servers=[kafka_server],
    value_serializer=lambda data: json.dumps(data).encode("utf-8")
)

print("Kafka connection initialized!")
print("AtmoSync IoT Sensor Simulator Started!")
print("Sensor data will be saved to CSV and sent to Kafka.")
print("Press Ctrl + C to stop.\n")

# ---------------------------------
# CSV Column Names
# ---------------------------------

fieldnames = [
    "container_id",
    "timestamp",
    "temperature_c",
    "humidity_percent",
    "vibration_g"
]

# ---------------------------------
# Generate and Stream Sensor Data
# ---------------------------------

try:
    while True:

        # Generate one sensor reading
        sensor_data = {
            "container_id": "CONTAINER_001",
            "timestamp": datetime.now().isoformat(),
            "temperature_c": round(random.uniform(4, 12), 2),
            "humidity_percent": round(random.uniform(40, 90), 2),
            "vibration_g": round(random.uniform(0.0, 1.5), 2)
        }

        # Save the same reading to CSV
        file_exists = output_file.exists()

        with open(output_file, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if not file_exists or output_file.stat().st_size == 0:
                writer.writeheader()

            writer.writerow(sensor_data)

        # Send the same reading to Kafka
        future = producer.send(kafka_topic, sensor_data)
        future.get(timeout=10)

        # Display the generated reading
        print("Sensor Reading:")
        print(json.dumps(sensor_data, indent=4))
        print("Saved to CSV and sent to Kafka successfully!\n")

        # Generate readings every 5 seconds
        time.sleep(5)

except KeyboardInterrupt:
    print("\nAtmoSync simulator stopped by user.")

except Exception as error:
    print("\nAn error occurred:", error)

finally:
    producer.flush()
    producer.close()
    print("Kafka connection closed.")
