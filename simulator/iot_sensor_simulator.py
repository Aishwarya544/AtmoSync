
import random
import time
import json
import csv
from datetime import datetime
from pathlib import Path

# AtmoSync project directory
project_folder = Path(__file__).resolve().parent.parent

# Save generated sensor data here
output_file = project_folder / "data" / "raw" / "sensor_readings.csv"

# Generate sensor readings continuously
print("AtmoSync IoT Sensor Simulator Started")
print("Press Ctrl + C to stop the simulator.\n")

try:
    while True:

        # Generate mock sensor readings
        sensor_data = {
            "container_id": "CONTAINER_001",
            "timestamp": datetime.now().isoformat(),
            "temperature_c": round(random.uniform(4, 12), 2),
            "humidity_percent": round(random.uniform(60, 90), 2),
            "vibration_g": round(random.uniform(0.0, 1.5), 2)
        }

        # Display readings
        print(json.dumps(sensor_data, indent=4))

        # Save readings to CSV
        file_exists = output_file.exists()

        with open(output_file, "a", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=sensor_data.keys()
            )

            if not file_exists:
                writer.writeheader()

            writer.writerow(sensor_data)

        print("Sensor reading saved successfully!\n")

        # Wait 5 seconds before the next reading
        time.sleep(5)

except KeyboardInterrupt:
    print("\nAtmoSync IoT Simulator stopped.")
