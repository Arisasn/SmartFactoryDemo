import network, time, json, ubinascii
from umqtt.simple import MQTTClient

WIFI_SSID = "YOUR_WIFI"
WIFI_PASS = "YOUR_PASS"
BROKER = "YOUR_MINI_PC_IP"
CAR_ID = "car1"

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            time.sleep(0.2)
    return wlan.ifconfig()[0]

ip = connect_wifi()
client_id = b"%s_%s" % (CAR_ID.encode(), ubinascii.hexlify(network.WLAN().config('mac')[-3:]))
mqtt = MQTTClient(client_id, BROKER)
mqtt.connect()
mqtt.subscribe(f"agv/{CAR_ID}/cmd")

while True:
    heartbeat = {"ip": ip, "status":"alive", "ts": time.time()}
    mqtt.publish(f"agv/{CAR_ID}/telemetry", json.dumps(heartbeat))
    mqtt.check_msg()
    time.sleep(1)
