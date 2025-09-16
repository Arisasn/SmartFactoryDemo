import threading, json, time
from flask import Flask, request, jsonify, render_template_string
import paho.mqtt.client as mqtt

BROKER = "localhost"
TOPICS = [("agv/+/telemetry", 0)]  # listen to all robot telemetry
state = {}  # {car_id: data}

def on_connect(client, userdata, flags, rc):
    client.subscribe(TOPICS)

def on_message(client, userdata, msg):
    try:
        car = msg.topic.split("/")[1]
        state[car] = json.loads(msg.payload.decode())
        state[car]["_ts"] = time.time()
    except:
        pass

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect(BROKER, 1883, 60)
threading.Thread(target=mqttc.loop_forever, daemon=True).start()

app = Flask(__name__)

HTML = """
<!doctype html>
<title>Smart Factory Dashboard</title>
<h1>AGV Control</h1>
<form method="post" action="/cmd">
Car ID: <input name="car" value="car1">
<button name="action" value="F">Forward</button>
<button name="action" value="L">Left</button>
<button name="action" value="R">Right</button>
<button name="action" value="S">Stop</button>
</form>
<pre id="out">Loading...</pre>
<script>
async function poll(){
  const r = await fetch('/status');
  document.getElementById('out').textContent = JSON.stringify(await r.json(), null, 2);
  setTimeout(poll, 1000);
}
poll();
</script>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/status")
def status():
    now = time.time()
    out = {}
    for car, s in state.items():
        age = round(now - s["_ts"], 1)
        s2 = dict(s)
        s2["age"] = age
        out[car] = s2
    return jsonify(out)

@app.post("/cmd")
def cmd():
    car = request.form.get("car", "car1")
    action = request.form.get("action", "S")
    mqttc.publish(f"agv/{car}/cmd", action)
    return ("", 204)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=False)
