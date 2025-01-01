from machine import Pin, SoftSPI
import GFX
import SSD1331
import ScreenWrite

'''Constants for initialization'''
SSD1331_PIN_CS  = 15
SSD1331_PIN_DC  = 32
SSD1331_PIN_RST = 14
SSD1331_PIN_SCK = 5 # Connects to SCL on the OLED display
SSD1331_PIN_MOSI = 19 # Connects to SDA on the OLED display
SSD1331_PIN_MISO = 21 # Just kinda exists lol
RED_PIN = 27
IR_PIN = 0 # Choose a pin for IR light
PHOTODIODE_PIN = 0 # Choose a pin for the diode MUST BE ADC1
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