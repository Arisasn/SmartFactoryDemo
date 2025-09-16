import sys, time, json, threading
import paho.mqtt.client as mqtt

BROKER = "localhost"   # or your mini PC IP
CAR_ID = sys.argv[1] if len(sys.argv) > 1 else "car1"

state = {"speed": 0, "mode": "idle"}

def on_cmd(client, userdata, msg):
    global state
    cmd = msg.payload.decode()
    if cmd == "F":
        state = {"speed": 150, "mode": "forward"}
    elif cmd == "L":
        state = {"speed": 100, "mode": "turn_left"}
    elif cmd == "R":
        state = {"speed": 100, "mode": "turn_right"}
    elif cmd == "S":
        state = {"speed": 0, "mode": "stop"}

def publish_loop(client):
    while True:
        tele = dict(state, ts=time.time())
        client.publish(f"agv/{CAR_ID}/telemetry", json.dumps(tele))
        time.sleep(0.5)

client = mqtt.Client()
client.on_message = on_cmd
client.connect(BROKER, 1883, 60)
client.subscribe(f"agv/{CAR_ID}/cmd")
threading.Thread(target=client.loop_forever, daemon=True).start()
publish_loop(client)
