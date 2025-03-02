import adafruit_dht
import board
import time
import json

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

from config import SHADOW_CLIENT, HOST_NAME, ROOT_CA, PRIVATE_KEY, CERT_FILE, SHADOW_HANDLER, RUN_TESTS

# DHT11 setup
dht = adafruit_dht.DHT11(board.D14)  
reading_timestamp = 0

def myShadowUpdateCallback(payload, responseStatus, token):
    print()
    
def createPayload():
    data = None
    
    try:
        temperature = dht.temperature
        humidity = dht.humidity
        reading_timestamp = time.time()
        
        # Create payload data dictionary
        data = {
            "temperature": round(temperature, 1),
            "humidity": round(humidity, 1),
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
            "reading_timestamp": reading_timestamp
        }
        
        
    except RuntimeError as error:
        print(f"Reading failed: {error.args[0]}")
    
    return data

try:
    myShadowClient = AWSIoTMQTTShadowClient(SHADOW_CLIENT)
    myShadowClient.configureEndpoint(HOST_NAME, 8883)
    myShadowClient.configureCredentials(ROOT_CA, PRIVATE_KEY, CERT_FILE)
    myShadowClient.configureConnectDisconnectTimeout(10)
    myShadowClient.configureMQTTOperationTimeout(5)
    
    myShadowClient.connect()
    
    myDeviceShadow = myShadowClient.createShadowHandlerWithName(SHADOW_HANDLER, True)
    
    while True:
        data = createPayload()
        
        if data:
            publish_timestamp = time.time()
            data["publish_timestamp"] = publish_timestamp
            
            reading_timestamp = data["reading_timestamp"]
            
            data["sensor_to_publish_latency_ms"] = round((publish_timestamp - reading_timestamp) * 1000, 2)
    
            shadow_json = json.dumps({"state": {"reported": data}})
            
            myDeviceShadow.shadowUpdate(shadow_json, myShadowUpdateCallback, 10)
            
            print(f"Created data: {data}")
            
            
        time.sleep(5.0)
        
except KeyboardInterrupt:
    print('Program stopped by user')
    
except Exception as e:
    print(f"Connection error: {e}")
    
finally:
    dht.exit()
    myShadowClient.disconnect()