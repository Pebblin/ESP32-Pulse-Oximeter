import umqtt1
import network
import sys

# Set up Adafruit connection
myMqttClient = "TestClient"
adafruitIoUrl = "io.adafruit.com"

# Change accordingly
adafruitUsername = ""
adafruitAioKey = ""

# Connect to Adafruit server
mqtt = umqtt1.MQTTClient(myMqttClient, adafruitIoUrl, 0, adafruitUsername, adafruitAioKey)
time.sleep(0.5)
mqtt.connect()

# CHANGE HERE
feedName = ""