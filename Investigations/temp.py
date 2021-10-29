'''
 Demonstrates RPI Pico DHT22 (AM2302) temperature / Humidity sensor measurement
 
 # DHT22 library is available at
 # https://github.com/danjperron/PicoDHT22
 
 # DHT22 Sensor pins
 * DHT22 Pin 1 to 3V3
 * DHT22 Pin 2 to GPIO2
 * DHT22 Pin 3 to NC
 * DHT22 Pin 4 to GND
  '''

from machine import Pin
from DHT22 import DHT22
import time

#Initialize the onboard LED as output
led = Pin(25, Pin.OUT)

# Initialize DHT22
dht22 = DHT22(Pin(4,Pin.IN,Pin.PULL_UP))

while True:
    T, H = dht22.read()
    #Write Humidity value. Convert the humidity into two decimal places.
    print(str('H: ' +"{:0.1f}".format(H)+ "%"), str('T: ' +"{:0.1f}".format(T)+ "C"))
    
    led.toggle()
    time.sleep_ms(200)
    led.value(T>30)
    
    # Wait for Five seconds. Then proceed to collect next sensor reading.
    time.sleep_ms(5000)