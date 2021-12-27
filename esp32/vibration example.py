from machine import Pin
import time

switch = Pin(23, Pin.IN)

while True:
    vibration = switch.value()
    if vibration:
        print("Vibrations!", end='\r')
        time.sleep(1)
    print("Quiet      ", end='\r')
