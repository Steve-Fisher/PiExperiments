from machine import Pin
from time import sleep

ledPin = 4;

p = Pin(ledPin, Pin.OUT)

p.value(True)
sleep(1)
p.value(False)
sleep(1)
