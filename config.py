# MQTT setup
MQTT_BROKER = "raspberrypi.local"
MQTT_PORT = 1883
MQTT_TOPIC = "binary/updates"

# AWS IoT setup
SHADOW_CLIENT = "myShadowClient10"
HOST_NAME = "a1mx9i1gtogccp-ats.iot.us-east-2.amazonaws.com"
ROOT_CA = "keys/AmazonRootCA1.pem"
PRIVATE_KEY = "keys/private.pem.key"
CERT_FILE = "keys/certificate.pem.crt"
SHADOW_HANDLER = "cis589_p2"

RUN_TESTS = False