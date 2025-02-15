import adafruit_dht
import board
import time
import json
import paho.mqtt.client as mqtt

# DHT11 setup
dht = adafruit_dht.DHT11(board.D14)

# MQTT setup
MQTT_BROKER = "raspberrypi.local"
MQTT_PORT = 1883
MQTT_TOPIC = "binary/updates"

# Initialize MQTT client
client = mqtt.Client(client_id="cis589")

try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    
    while True:
        try:
            temperature = dht.temperature
            humidity = dht.humidity
            
            # Create payload
            data = {
                "temperature": round(temperature, 1),
                "humidity": round(humidity, 1),
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Publish
            payload = json.dumps(data)
            client.publish(MQTT_TOPIC, payload)
            
            print(f"Published: {payload}")
            
        except RuntimeError as error:
            print(f"Reading failed: {error.args[0]}")
        
        time.sleep(2.0)

except KeyboardInterrupt:
    print('Program stopped by user')
    
except Exception as e:
    print(f"Connection error: {e}")
    
finally:
    # Clean up
    dht.exit()
    client.loop_stop()
    client.disconnect()
    print("Disconnected from MQTT broker")