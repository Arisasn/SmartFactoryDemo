import sys, time, json, math, threading
import paho.mqtt.client as mqtt

BROKER = "localhost"
CAR_ID = sys.argv[1] if len(sys.argv) > 1 else "car1"
x = float(sys.argv[2]) if len(sys.argv) > 2 else 120.0
y = float(sys.argv[3]) if len(sys.argv) > 3 else 140.0
heading = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0  # deg

# Motion params
FWD_SPEED = 80.0          # px/s
TURN_RATE = 90.0          # deg/s
AUTO_SPEED = 70.0
AUTO_TURN = 80.0
AVOID_RANGE = 45.0        # px
AVOID_TURN = 120.0        # deg/s

mode = "idle"             # manual: forward/turn_left/turn_right/stop; auto: auto_circle/auto_square/auto_avoid
speed = 0.0

# For square auto
sq_phase = "forward"      # forward -> turn -> forward ...
sq_side_time = 1.6        # seconds moving forward per side
sq_turn_left = True
sq_timer = 0.0
sq_turn_accum = 0.0

# Track peers for avoidance
peers = {}  # id -> {"x":..,"y":..,"ts":..}

def on_cmd(client, userdata, msg):
    global mode, speed, sq_phase, sq_timer, sq_turn_accum
    cmd = msg.payload.decode().strip().upper()
    if cmd in ("F","L","R","S","MAN"):
        # manual modes
        if cmd == "F":
            mode, speed = "forward", FWD_SPEED
        elif cmd == "L":
            mode, speed = "turn_left", 0.0
        elif cmd == "R":
            mode, speed = "turn_right", 0.0
        elif cmd == "S":
            mode, speed = "stop", 0.0
        elif cmd == "MAN":
            mode, speed = "idle", 0.0
        # reset square timers
        sq_phase, sq_timer, sq_turn_accum = "forward", 0.0, 0.0
    elif cmd == "A1":
        mode, speed = "auto_circle", AUTO_SPEED
    elif cmd == "A2":
        mode, speed = "auto_square", AUTO_SPEED
        sq_phase, sq_timer, sq_turn_accum = "forward", 0.0, 0.0
    elif cmd == "A3":
        mode, speed = "auto_avoid", AUTO_SPEED

def on_peer(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        pid = data.get("id")
        if pid and pid != CAR_ID and "x" in data and "y" in data:
            peers[pid] = {"x": float(data["x"]), "y": float(data["y"]), "ts": time.time()}
    except Exception:
        pass

def nearest_peer():
    """Return (dist, dx, dy) to closest peer within stale window, else (None,0,0)."""
    now = time.time()
    best = None
    for p,data in peers.items():
        if now - data["ts"] > 1.0:  # stale
            continue
        dx, dy = data["x"] - x, data["y"] - y
        d = math.hypot(dx, dy)
        if best is None or d < best[0]:
            best = (d, dx, dy)
    return best if best else (None, 0.0, 0.0)

def physics_loop(client):
    global x, y, heading, mode, speed, sq_phase, sq_timer, sq_turn_accum
    last = time.time()
    pub_acc = 0.0
    while True:
        now = time.time()
        dt = now - last
        last = now

        # --- AUTO MODES BEHAVIOR ---
        if mode == "auto_circle":
            # forward + gentle continuous turn
            speed = AUTO_SPEED
            heading += AUTO_TURN * dt

        elif mode == "auto_square":
            if sq_phase == "forward":
                speed = AUTO_SPEED
                sq_timer += dt
                if sq_timer >= sq_side_time:
                    sq_phase = "turn"
                    sq_timer = 0.0
                    sq_turn_accum = 0.0
            else:  # turn 90 deg
                speed = 0.0
                turn_sign = -1 if sq_turn_left else 1
                dtheta = turn_sign * TURN_RATE * dt
                heading += dtheta
                sq_turn_accum += abs(dtheta)
                if sq_turn_accum >= 90.0:
                    sq_phase = "forward"
                    sq_timer = 0.0
                    sq_turn_left = not sq_turn_left

        elif mode == "auto_avoid":
            # default go forward, but steer away if someone is close
            speed = AUTO_SPEED
            dist, dx, dy = nearest_peer()
            if dist is not None and dist < AVOID_RANGE:
                # steer away from peer: rotate opposite of relative angle
                peer_angle = math.degrees(math.atan2(dy, dx))
                # desired avoidance: choose rotation that increases angle difference quickly
                diff = (peer_angle - heading + 540) % 360 - 180  # [-180,180]
                turn_dir = -1 if diff > 0 else 1  # turn opposite direction
                heading += turn_dir * AVOID_TURN * dt
                # also throttle forward when too close
                if dist < AVOID_RANGE * 0.7:
                    speed = AUTO_SPEED * 0.5

        # --- MANUAL BEHAVIOR (from previous version) ---
        if mode == "forward":
            rad = math.radians(heading)
            x += math.cos(rad) * speed * dt
            y += math.sin(rad) * speed * dt
        elif mode == "turn_left":
            heading -= TURN_RATE * dt
        elif mode == "turn_right":
            heading += TURN_RATE * dt
        elif mode in ("stop","idle"):
            pass

        # common forward movement for auto modes
        if mode.startswith("auto_"):
            rad = math.radians(heading)
            x += math.cos(rad) * speed * dt
            y += math.sin(rad) * speed * dt

        # tidy heading
        if heading > 180: heading -= 360
        if heading < -180: heading += 360

        # publish ~5Hz
        pub_acc += dt
        if pub_acc >= 0.2:
            tele = {
                "id": CAR_ID, "x": round(x,1), "y": round(y,1),
                "heading": round(heading,1), "mode": mode,
                "speed": round(speed,1), "ts": now
            }
            client.publish(f"agv/{CAR_ID}/telemetry", json.dumps(tele))
            pub_acc = 0.0

        time.sleep(0.01)

client = mqtt.Client()
client.on_message = on_cmd
client.connect(BROKER, 1883, 60)
client.subscribe(f"agv/{CAR_ID}/cmd")

# Also listen to all telemetry for avoidance
client.message_callback_add("agv/+/telemetry", on_peer)
client.subscribe("agv/+/telemetry")

threading.Thread(target=client.loop_forever, daemon=True).start()
physics_loop(client)
