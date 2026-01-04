import time
import random
from database import insert_data

SENSOR_ID = "sensor-01"

print("Sensor started...")

while True:
    data = {
        "sensor_id": SENSOR_ID,
        "temperature": round(random.uniform(20, 35), 2),
        "humidity": round(random.uniform(30, 60), 2),
        "ts": int(time.time() * 1000)
    }

    insert_data(data)
    print("Inserted:", data)
    time.sleep(2)