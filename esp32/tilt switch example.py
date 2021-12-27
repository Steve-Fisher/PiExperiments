from machine import Pin
import time

switch = Pin(23, Pin.IN)

while True:
    state = not(switch.value())
    print("Switch is " + ("on " if state else "off"), end='\r')
    time.sleep(0.2)
