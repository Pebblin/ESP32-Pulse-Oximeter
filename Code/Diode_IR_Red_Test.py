from machine import Pin, SoftSPI, ADC, RTC
from time import sleep

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

IRD = ADC(Pin(36,mode=Pin.IN))
IRD.atten(ADC.ATTN_11DB)       #Full range: 3.3v
REDD = ADC(Pin(39,mode=Pin.IN))
REDD.atten(ADC.ATTN_11DB)       #Full range: 3.3v


for i in range(50):
    RED(0)
    RED2(0)
    IR(1)
    sleep(0.04)
    IR_Val = IRD.read()
    RED(1)
    RED2(1)
    IR(0)
    sleep(0.04)
    print("IR: {} | RED: {}".format(IR_Val,REDD.read()))
    
