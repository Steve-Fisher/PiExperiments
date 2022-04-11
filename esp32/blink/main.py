from machine import Pin
from time import sleep

led = Pin(2, Pin.OUT)
i = 0

while i<10:
  led.value(not led.value())
  sleep(0.5)
  i+=1

led.value(0)