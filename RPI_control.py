import json
import os
import socket
import uuid
import paho.mqtt.client as mqtt

BROKER = "10.128.48.5"
PORT = 1883

def get_device_id():
    # Expects hostnames like "rpi-A01" or "RPI-A01" → "A01"
    try:
        h = socket.gethostname()
        return h.replace("rpi-", "").replace("RPI-", "")
    except Exception:
        return "unknown"

DEVICE_ID = get_device_id()
TOPIC_CONTROL = f"rpi/control/{DEVICE_ID}"
TOPIC_ACK     = f"rpi/control/ack/{DEVICE_ID}"
TOPIC_CONFIRM = f"rpi/control/confirm/{DEVICE_ID}"

pending = {}  # request_id -> command


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[OK] Connected to MQTT {BROKER}:{PORT} as device '{DEVICE_ID}'")
        client.subscribe(TOPIC_CONTROL)
        client.subscribe(TOPIC_CONFIRM)
        print(f"[SUB] {TOPIC_CONTROL}")
        print(f"[SUB] {TOPIC_CONFIRM}")
    else:
        print(f"[ERR] MQTT connect rc={rc}")


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        command = data.get("command", "").lower()
        print(f"Received command: {command}")
        if command == "reboot":
            print("Rebooting now...")
            os.system("sudo reboot")
        elif command == "shutdown":
            print("Shutting down now... - not really")
            #os.system("sudo shutdown now")
    except Exception as e:
        print(f"Error: {e}")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.loop_forever()


