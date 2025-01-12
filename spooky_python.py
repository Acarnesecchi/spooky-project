import paho.mqtt.client as mqtt
import serial  # Avoid conflicts with other files/modules
import json

# MQTT setup
broker_address = "157.245.24.199"  # Replace with your broker address
port = 1883
client = mqtt.Client(
    callback_api_version=2,
    client_id="RadarSensor",
    protocol=mqtt.MQTTv311,
    transport="tcp"
)
client.connect(broker_address, port)

# Serial setup
serial_port = "COM7"  # Adjust to match your COM port
baud_rate = 115200
ser = serial.Serial(serial_port, baud_rate)

# Function to publish data to MQTT
def publish_to_mqtt(topic, message):
    client.publish(topic, message)

# Read and parse serial data
try:
    while True:
        if ser.in_waiting > 0:
            try:
                line = ser.readline().decode("utf-8").strip()
            except UnicodeDecodeError:
                print("Failed to decode serial data.")
                continue

            if line.startswith("MQTT:"):
                try:
                    # Parse MQTT topic and message
                    _, topic_message = line.split("MQTT:", 1)
                    topic, message = topic_message.split(":", 1)
                    if topic.strip() == "existance/direction":
                        values = message.split()
                        json_data = {"X": float(values[0]), "Y": float(values[1]), "Z": float(values[2])}
                        publish_to_mqtt(topic.strip(), json.dumps(json_data))
                    elif topic.strip() == "existance/distance":
                        publish_to_mqtt(topic.strip(), float(message.strip())*100)
                    else:
                        value = float(message.split(" ")[0])
                        publish_to_mqtt(topic.strip(), float(value))
                    print(f"Published to {topic.strip()}: {message.strip()}")
                except ValueError:
                    print("Malformed MQTT message format.")
                    print(line)
                    continue

except KeyboardInterrupt:
    print("Exiting...")
    ser.close()
    client.disconnect()
