from machine import Pin, ADC
from time import sleep

pot = ADC(Pin(39,mode=Pin.IN))
pot.atten(ADC.ATTN_11DB)       #Full range: 3.3v

while True:
  pot_value = pot.read()
  print(pot_value)
  sleep(0.1)

