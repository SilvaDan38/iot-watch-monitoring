import json
import time
import random
import uuid
import paho.mqtt.client as mqtt

BROKER="mqtt"

client = mqtt.Client()
client.connect(BROKER,1883,60)

devices = [f"watch_{i}" for i in range(30)]

while True:
    for d in devices:
        payload = {
            "device_id": d,
            "heart_rate": random.randint(60,140),
            "steps": random.randint(0,20),
            "battery": random.randint(20,100),
            "trace_id": str(uuid.uuid4())
        }

        client.publish("iot/watch", json.dumps(payload))

    time.sleep(5)
