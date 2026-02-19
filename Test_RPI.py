import paho.mqtt.client as mqtt
import subprocess
import socket
import psutil
import time
import json

client = mqtt.Client()

def get_cpu_load():
    return round(psutil.cpu_percent(interval=1), 4)

def get_ram_usage():
    mem = psutil.virtual_memory()
    return round(mem.used / (1024 ** 3), 2)  # in GB

def get_disk_usage():
    disk = psutil.disk_usage('/')
    return round(disk.used / (1024 ** 3), 2)  # in GB

def get_temp():
    try:
        output = subprocess.check_output(["/usr/bin/vcgencmd", "measure_temp"]).decode()
        return float(output.strip().replace("temp=", "").replace("'C", ""))
    except:
        return 0.0

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "0.0.0.0"

def get_device_id():
    try:
        hostname = socket.gethostname()
        return hostname.replace("RPI-", "")
    except:
        return "unknown"

broker = "10.128.48.5"
port = 1883
topic = "rpi/data"
client.connect(broker, port)

while True:
    message = {
        "id": get_device_id(),
        "cpuLoad": f"{get_cpu_load()}%",
        "ram": f"{get_ram_usage()}GB",
        "diskUsage": f"{get_disk_usage()}GB",
        "cpuTemp": get_temp(),
        "ip": get_ip_address(),
    }
    client.publish(topic, json.dumps(message))
    time.sleep(30)
