import time, json, threading
import paho.mqtt.client as mqtt

BROKER = "localhost"
CAR_ID = "car1"
state = {"speed":0, "mode":"idle"}

def on_msg(client, userdata, msg):
    global state
    cmd = msg.payload.decode()
    if cmd == "F":
        state = {"speed":150, "mode":"forward"}
    elif cmd == "L":
        state = {"speed":100, "mode":"turn_left"}
    elif cmd == "R":
        state = {"speed":100, "mode":"turn_right"}
    elif cmd == "S":
        state = {"speed":0, "mode":"stop"}

def pub_loop(client):
    while True:
        telemetry = dict(state, ts=time.time())
        client.publish(f"agv/{CAR_ID}/telemetry", json.dumps(telemetry))
        time.sleep(0.5)

client = mqtt.Client()
client.on_message = on_msg
client.connect(BROKER, 1883, 60)
client.subscribe(f"agv/{CAR_ID}/cmd")
threading.Thread(target=client.loop_forever, daemon=True).start()
pub_loop(client)
