# ESP32-Pulse-Oximeter
Contains micropython files used for our pulse oximeter implementation.

## Code
- main.py is the main driver of the oximeter. Certain lines have been changed to remove sensitive information.
- Files containing "_test" were used for testing individual functions of the oximeter.
- GFX.py is borrowed from adafruit's depreciated repository "micropython-adafruit-gfx"
- rgb.py and SSD1331.py are borrowed from adafruit's depreciated repository "micropython-adafruit-rgb-display"
- ScreenWrite.py describes a custom class used to communicate with the display, which was a HiLetgo 0.95'' SPI OLED display. SPI was the protocol of choice here because previous labs had us work with I2C and UART, and we wanted additional experience.
- umqtt1.py is adapted from micropython's simple.py from the umqtt.simple folder in the "micropython-lib" repository.