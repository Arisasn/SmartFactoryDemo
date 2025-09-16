import threading, json, time
from flask import Flask, request, jsonify, render_template_string
import paho.mqtt.client as mqtt

BROKER = "localhost"
TOPICS = [("agv/+/telemetry", 0)]
state = {}  # {car_id: {..., _ts: float}}

def on_connect(c, u, f, rc):
    c.subscribe(TOPICS)

def on_message(c, u, msg):
    try:
        car = msg.topic.split("/")[1]
        data = json.loads(msg.payload.decode())
        data["_ts"] = time.time()
        state[car] = data
    except Exception:
        pass

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect(BROKER, 1883, 60)
threading.Thread(target=mqttc.loop_forever, daemon=True).start()

app = Flask(__name__)

HTML = """
<!doctype html>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Smart Factory Dashboard</title>
<style>
body { font-family: system-ui, sans-serif; margin: 16px; }
.wrap { display:flex; gap:18px; flex-wrap:wrap; align-items:flex-start; }
.card { padding:12px; border:1px solid #ddd; border-radius:10px; }
#map { border:1px solid #ccc; border-radius:10px; }
button { margin-right:6px; }
</style>
<h1>Smart Factory Dashboard</h1>
<div class="wrap">
  <div class="card">
    <h3>Controls</h3>
    <form method="post" action="/cmd" style="margin-bottom:8px">
      <label>Car ID: <input name="car" value="car1" style="width:100px"></label><br><br>
      <div style="margin-bottom:6px"><strong>Manual:</strong></div>
      <button name="action" value="F">Forward</button>
      <button name="action" value="L">Left</button>
      <button name="action" value="R">Right</button>
      <button name="action" value="S">Stop</button>
      <button name="action" value="MAN">Manual Mode</button>
      <br><br>
      <div style="margin-bottom:6px"><strong>Auto:</strong></div>
      <button name="action" value="A1">Circle</button>
      <button name="action" value="A2">Square</button>
      <button name="action" value="A3">Avoid</button>
    </form>
    <div>
      <button onclick="spawn('car1',120,140,0)">Spawn car1</button>
      <button onclick="spawn('car2',300,260,90)">Spawn car2</button>
      <button onclick="spawn('car3',220,120,-90)">Spawn car3</button>
    </div>
  </div>

  <div class="card">
    <h3>Map</h3>
    <canvas id="map" width="520" height="360"></canvas>
  </div>

  <div class="card" style="flex:1; min-width:320px;">
    <h3>Status</h3>
    <pre id="out">Loading...</pre>
  </div>
</div>

<script>
async function fetchStatus(){
  const r = await fetch('/status');
  const data = await r.json();
  document.getElementById('out').textContent = JSON.stringify(data, null, 2);
  drawMap(data);
}

function drawMap(data){
  const cv = document.getElementById('map');
  const ctx = cv.getContext('2d');
  ctx.clearRect(0,0,cv.width,cv.height);

  // grid
  ctx.strokeStyle = '#eee';
  for(let x=0;x<cv.width;x+=40){ ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,cv.height); ctx.stroke(); }
  for(let y=0;y<cv.height;y+=40){ ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(cv.width,y); ctx.stroke(); }

  // draw each car
  for (const [id, s] of Object.entries(data)){
    const x = s.x ?? 0, y = s.y ?? 0, h = (s.heading ?? 0) * Math.PI/180;
    // body
    ctx.fillStyle = '#222';
    ctx.beginPath();
    ctx.arc(x, y, 10, 0, Math.PI*2);
    ctx.fill();
    // heading
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x + Math.cos(h)*18, y + Math.sin(h)*18);
    ctx.strokeStyle = '#222';
    ctx.stroke();
    // label
    ctx.fillStyle = '#008';
    ctx.fillText(id + " ("+(s.mode||"")+")", x+12, y-12);
  }
}

function loop(){ fetchStatus().catch(()=>{}); setTimeout(loop, 500); }
loop();

// helper to spawn sims
async function spawn(id,x,y,h){
  await fetch('/spawn', {method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({id, x, y, h})
  });
}
</script>
"""

@app.get("/")
def home():
    return render_template_string(HTML)

@app.get("/status")
def status():
    now = time.time()
    out = {}
    for k,v in state.items():
        vv = dict(v)
        vv["age"] = round(now - v.get("_ts", now), 2)
        out[k] = vv
    return jsonify(out)

@app.post("/cmd")
def cmd():
    car = request.form.get("car","car1")
    action = request.form.get("action","S")
    mqttc.publish(f"agv/{car}/cmd", action)
    return ("", 204)

# optional helper: start a sim via server (requires sim_car.py available)
import subprocess, os, sys as _sys
@app.post("/spawn")
def spawn():
    data = (request.get_json(silent=True) or {})
    cid = str(data.get("id","carX"))
    x = data.get("x",120); y = data.get("y",140); h = data.get("h",0)
    # run in background
    subprocess.Popen(["python3", os.path.join(os.path.dirname(__file__), "..", "code", "sim", "sim_car.py"),
                      cid, str(x), str(y), str(h)])
    return jsonify(ok=True, started=cid)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=False)
