from machine import Pin, SoftSPI, ADC, RTC
import umqtt1
import esp
import network
import time
import GFX
import SSD1331
import ScreenWrite
import math
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

mqtt.publish(feedName,"Oximeter has been started")


'''Constants for initialization'''
SSD1331_PIN_CS  = 15
SSD1331_PIN_DC  = 32
SSD1331_PIN_RST = 14
SSD1331_PIN_SCK = 5 # Connects to SCL on the OLED display
SSD1331_PIN_MOSI = 19 # Connects to SDA on the OLED display
SSD1331_PIN_MISO = 21 # Just kinda exists lol
RED_PIN = 27
RED2_PIN = 4
IR_PIN = 33 
PHOTODIODE_PIN_RED = 39 # Choose a pin for the diode MUST BE ADC1
PHOTODIODE_PIN_IR = 36
width = 96
height = 64
        
'''OLED Display Initialization'''
# SPI Pin assignment 
spi = SoftSPI(mosi=Pin(SSD1331_PIN_MOSI), sck=Pin(SSD1331_PIN_SCK), miso=Pin(SSD1331_PIN_MISO), polarity=1, phase=1)

# Generate a display object
display = SSD1331.SSD1331(spi, dc=Pin(SSD1331_PIN_DC), cs=Pin(SSD1331_PIN_CS), rst=Pin(SSD1331_PIN_RST))

# Generate a GFX object
gfx = GFX.GFX(width, height, pixel=display.pixel, hline=display.hline, vline=display.vline)

# Generate a screenwrite object
sw = ScreenWrite.ScreenWrite()

# First time OLED setup
sw.backgroundRefresh(display)
sw.labels(gfx)
sw.write(gfx)

'''Oximeter Initialization'''
# Generate pin objects + ADC object
RED = Pin(RED_PIN, mode=Pin.OUT)
RED2 = Pin(RED2_PIN, mode=Pin.OUT)
IR = Pin(IR_PIN, mode=Pin.OUT)
PHOTODIODE_RED = ADC(Pin(PHOTODIODE_PIN_RED, mode=Pin.IN))
PHOTODIODE_RED.atten(ADC.ATTN_11DB) # Change resolution of measurements
PHOTODIODE_IR = ADC(Pin(PHOTODIODE_PIN_IR, mode=Pin.IN))
PHOTODIODE_IR.atten(ADC.ATTN_11DB) # Change resolution of measurements

# Constant initialization
MAX_PERIOD_SIZE = 80
MAX_MEASURES = 10
SAMPLE_SIZE = 4
RISE_THRESHOLD = 3
T = 20

# Variable initialization
POINTER = 0
MEASUREMENT_POINTER = 0
IR_SUM = 0
RED_SUM = 0
SAMPLES_TAKEN = 0
SAMPLES = 0
FINGER_STATUS = False
RISE_COUNT = 0
RISING = False
CURRENT_MEASUREMENT = 0
LAST_BEAT = 0
PREV_IR_VALUE = 0

# List initialization
IR_MM = [0] * MAX_PERIOD_SIZE
RED_MM = [0] * MAX_PERIOD_SIZE
R_MEASURES = [0] * MAX_MEASURES
BEAT_PERIOD_MEASURES = [0] * MAX_MEASURES
IR_SAMPLES = [0] * SAMPLE_SIZE
RED_SAMPLES = [0] * SAMPLE_SIZE

'''Define the method that loops permanently'''
while True:
    # Reset/Initialize value counters
    IR_VALUE = 0
    RED_VALUE = 0
    
    # Turn the IR on and the red RED off
    IR(1)
    RED(0)
    RED2(0)
    
    # Reset/Initialize IR counters
    NS = 0
    START_TIME = time.ticks_ms()
    
    # Take readings
    while time.ticks_ms() < START_TIME + T:
        NS += 1
        IR_VALUE += PHOTODIODE_IR.read()
        # print(PHOTODIODE_IR.read())
    
    # Add latest measurement to the list and remove oldest and calculates average
    IR_SAMPLES[POINTER] = IR_VALUE / NS
    LAST_IR = sum(IR_SAMPLES) / SAMPLE_SIZE
    
    # Turn the red LED on and the IR off
    IR(0)
    RED(1)
    RED2(1)
    
    # Reset/Initialize Red counters
    NS = 0
    START_TIME = time.ticks_ms()
    
    # Take readings
    while time.ticks_ms() < START_TIME + T:
        NS += 1
        RED_VALUE += PHOTODIODE_RED.read()
        # print(PHOTODIODE_RED.read())

        
    # Add latest measurement to the list and remove oldest and calculates average
    RED_SAMPLES[POINTER] = RED_VALUE / NS
    LAST_RED = sum(IR_SAMPLES) / SAMPLE_SIZE


    # Save all samples of a period for IR and Red
    IR_MM[MEASUREMENT_POINTER] = LAST_IR
    RED_MM[MEASUREMENT_POINTER] = LAST_RED
    
    # Increment the measurement pointer and reset if it reaches its max value
    MEASUREMENT_POINTER += 1
    MEASUREMENT_POINTER %= MAX_PERIOD_SIZE
    
    # Increment counter
    SAMPLES_TAKEN += 1
    
    # If 4 samples have been taken
    if SAMPLES_TAKEN >= SAMPLES:
        # Reset counter
        SAMPLES_TAKEN = 0
        
        # Initialize variables
        IR_MAX = 0;
        IR_MIN = 4095;
        RED_MAX = 0;
        RED_MIN = 4095;
        
        for i in range(SAMPLE_SIZE):
            # Set min/max values for IR measurements
            if IR_SAMPLES[i] > IR_MAX:
                IR_MAX = IR_SAMPLES[i]
            if IR_SAMPLES[i] < IR_MIN:
                IR_MIN = IR_SAMPLES[i]
                
            # Set min/max values for LED measurements
            if RED_SAMPLES[i] > RED_MAX:
                RED_MAX = RED_SAMPLES[i]
            if RED_SAMPLES [i] < RED_MIN:
                RED_MIN = RED_SAMPLES[i]
        
        # Reset sample vectors
        IR_MM = [0] * MAX_PERIOD_SIZE
        RED_MM = [0] * MAX_PERIOD_SIZE
        
        # Perform R calculation
        try: 
            R = ((RED_MAX - RED_MIN) / RED_MIN) / ((IR_MAX - IR_MIN) / IR_MIN)
        except:
            R = 0
        
    # Check if the finger is placed in the oximeter
    # Note: Red will be < IR if finger is missing
    if LAST_RED < LAST_IR:
        FINGER_STATUS = False
    else:
        FINGER_STATUS = True
        
    # Reset/Initialize average R and BPM counters
    AVG_R = 0
    AVG_BPM = 0
    
    # Check for BPM if finger is present
    # Note: A rising curve indicates a heartbeat
    if FINGER_STATUS:
        if LAST_IR > PREV_IR_VALUE:
            RISE_COUNT += 1
            
            if not RISING and RISE_COUNT > RISE_THRESHOLD:
                RISING = True
                
                # Store measurements
                R_MEASURES[CURRENT_MEASUREMENT] = R
                BEAT_PERIOD_MEASURES[CURRENT_MEASUREMENT] = time.ticks_ms() - LAST_BEAT
                LAST_BEAT = time.ticks_ms()
                
                # Calculate average period
                PERIOD = 0
                for i in range(MAX_MEASURES):
                    PERIOD += BEAT_PERIOD_MEASURES[i]
                
                PERIOD = PERIOD / MAX_MEASURES # Average period calculation
                SAMPLES = PERIOD / (2 * T) # 2 * the amount of time
                
                # Reset/Initialize 'C' value and average period
                AVG_PERIOD = 0
                C = 0 # C stores the number of good measures (not floating more than 10%) in the last 10 peaks
                 
                for i in range(MAX_MEASURES - 1):
                    if BEAT_PERIOD_MEASURES[i + 1] < BEAT_PERIOD_MEASURES[i] * 1.1 and BEAT_PERIOD_MEASURES[i + 1] > BEAT_PERIOD_MEASURES[i] * 0.9:
                        C += 1
                        AVG_PERIOD += BEAT_PERIOD_MEASURES[i]
                        AVG_R += R_MEASURES[i]
                        
                # Increment/Reset the current measurement
                CURRENT_MEASUREMENT += 1
                CURRENT_MEASUREMENT %= MAX_MEASURES
                
                # Calculations
                try:
                    AVG_BPM = 60000 / (AVG_PERIOD / C)
                    AVG_R = AVG_R / C
                except:
                    AVG_BPM = 0
                    AVG_R = 0
                
                # If there are at least 5 good measures, show bpm and O2
                # print(C)
                if C > 4:
                    o = int(abs(-20 * R + 104))
                    try:
                        # print(AVG_BPM)
                        # print(o)
                        sw.write(gfx,str(int(AVG_BPM)),str(o))
                        
                        # Publish a message to MQTT and print in console
                        if o > 90:
                            mqtt.publish(feedName,"BPM: {} | O2%: {}%".format(int(abs(AVG_BPM)),o))
                            print("BPM: {} | O2%: {}%".format(int(abs(AVG_BPM)),o))
                        else:
                            mqtt.publish(feedName,"Critical")
                            print("Critical")
                            print("BPM: {} | O2%: {}%".format(int(abs(AVG_BPM)),o))
                        
                    except:
                        # print(AVG_BPM)
                        # print(o)
                        if o > 90:
                            mqtt.publish(feedName,"BPM: {} | O2%: {}%".format(int(abs(AVG_BPM)),o))
                            print("BPM: {} | O2%: {}%".format(int(abs(AVG_BPM)),o))
                        else:
                            mqtt.publish(feedName,"Critical")
                            print("Critical")
                            print("BPM: {} | O2%: {}%".format(int(abs(AVG_BPM)),o))
                else:
                    mqtt.publish(feedName,"Not enough good measurements were taken in the last measurement cycle")
                    print("Not enough good measurements were taken in the last measurement cycle")

        else:
            RISING = False
            RISE_COUNT = 0
                    
        PREV_IR_VALUE = LAST_IR
    
    # Increment/Reset pointer
    POINTER += 1
    POINTER %= SAMPLE_SIZE


