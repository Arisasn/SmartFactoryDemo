import paho.mqtt.client as mqtt

BROKER = "localhost"

def on_message(client, userdata, msg):
    print(f"[{msg.topic}] {msg.payload.decode()}")

client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.subscribe("agv/#")

print("Listening to MQTT topics...")
client.loop_forever()
