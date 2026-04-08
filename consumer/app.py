# ✅ Variáveis de ambiente ANTES de qualquer import do ddtrace
import os
os.environ["DD_AGENT_HOST"] = "datadog-agent"
os.environ["DD_TRACE_AGENT_PORT"] = "8126"
os.environ["DD_SERVICE"] = "iot-consumer"
os.environ["DD_ENV"] = "docker"
os.environ["DD_VERSION"] = "1.0.0"

# ✅ Só depois importa e inicializa
from ddtrace import tracer, patch_all
patch_all()  # ← descomentado

import json
import logging
import paho.mqtt.client as mqtt
from datadog import initialize, statsd

logging.basicConfig(level=logging.INFO)
initialize(statsd_host="datadog-agent", statsd_port=8125)

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)

    with tracer.trace("iot.consume") as span:
        span.set_tag("device_id", data["device_id"])
        span.set_tag("trace_id", data["trace_id"])
        span.set_tag("env", "docker")

        statsd.gauge("iot.watch.heart_rate", data["heart_rate"], tags=[f"device:{data['device_id']}"])
        statsd.gauge("iot.watch.battery",     data["battery"],    tags=[f"device:{data['device_id']}"])
        statsd.increment("iot.watch.steps",   data["steps"],      tags=[f"device:{data['device_id']}"])

        logging.info(f"device={data['device_id']} hr={data['heart_rate']} battery={data['battery']} trace={data['trace_id']}")

client = mqtt.Client()
client.connect("mqtt", 1883, 60)
client.subscribe("iot/watch")
client.on_message = on_message
client.loop_forever()