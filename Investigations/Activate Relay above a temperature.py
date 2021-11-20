from DHT22 import DHT22
from machine import Pin
import time

dht22 = DHT22(Pin(4,Pin.IN,Pin.PULL_UP))
r = Pin(14, Pin.OPEN_DRAIN)

while (True):
    T, H = dht22.read()
    r(T < 28)
    print(T)
    time.sleep_ms(2000)
    