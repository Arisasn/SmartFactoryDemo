import sys, time, json, math, threading
import paho.mqtt.client as mqtt

BROKER = "localhost"
CAR_ID = sys.argv[1] if len(sys.argv) > 1 else "car1"
# Optional CLI args: x y heading
x = float(sys.argv[2]) if len(sys.argv) > 2 else 100.0
y = float(sys.argv[3]) if len(sys.argv) > 3 else 100.0
heading = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0  # degrees

# Simple motion model
mode = "idle"
speed = 0.0                 # px/s
FWD_SPEED = 80.0            # px/s
TURN_RATE = 90.0            # deg/s

def on_cmd(client, userdata, msg):
    global mode, speed
    cmd = msg.payload.decode().strip().upper()
    if cmd == "F":
        mode, speed = "forward", FWD_SPEED
    elif cmd == "L":
        mode, speed = "turn_left", 0.0
    elif cmd == "R":
        mode, speed = "turn_right", 0.0
    elif cmd == "S":
        mode, speed = "stop", 0.0

def physics_loop(client):
    global x, y, heading, mode, speed
    last = time.time()
    pub_acc = 0.0
    while True:
        now = time.time()
        dt = now - last
        last = now

        # Update pose
        if mode == "forward":
            rad = math.radians(heading)
            x += math.cos(rad) * speed * dt
            y += math.sin(rad) * speed * dt
        elif mode == "turn_left":
            heading -= TURN_RATE * dt
        elif mode == "turn_right":
            heading += TURN_RATE * dt

        # Keep heading tidy
        if heading > 180: heading -= 360
        if heading < -180: heading += 360

        # Publish telemetry at ~5 Hz
        pub_acc += dt
        if pub_acc >= 0.2:
            tele = {
                "id": CAR_ID,
                "x": round(x, 1),
                "y": round(y, 1),
                "heading": round(heading, 1),
                "mode": mode,
                "speed": round(speed, 1),
                "ts": now
            }
            client.publish(f"agv/{CAR_ID}/telemetry", json.dumps(tele))
            pub_acc = 0.0

        time.sleep(0.01)

client = mqtt.Client()
client.on_message = on_cmd
client.connect(BROKER, 1883, 60)
client.subscribe(f"agv/{CAR_ID}/cmd")
threading.Thread(target=client.loop_forever, daemon=True).start()
physics_loop(client)
