from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime

# Connect Python to Kafka
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda data: json.dumps(data).encode("utf-8")
)

topic = "container-sensor-data"

print("AtmoSync Kafka Producer Started!")

try:
    while True:
        sensor_data = {
            "container_id": "CONT001",
            "timestamp": datetime.now().isoformat(),
            "temperature_c": round(random.uniform(20, 35), 2),
            "humidity_percent": round(random.uniform(50, 90), 2),
            "vibration_g": round(random.uniform(0.1, 1.0), 2)
        }

        producer.send(topic, sensor_data)

        print("Sent:", sensor_data)

        time.sleep(5)

except KeyboardInterrupt:
    print("Producer stopped.")

finally:
    producer.flush()
    producer.close()