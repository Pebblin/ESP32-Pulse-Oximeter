from machine import Pin

'''Constants for initialization'''
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

# Generate pin objects + ADC object
RED = Pin(RED_PIN, mode=Pin.OUT)
RED2 = Pin(RED2_PIN, mode=Pin.OUT)
IR = Pin(IR_PIN, mode=Pin.OUT)

RED(1)
RED2(1)
IR(1)
