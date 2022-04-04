try:
  import usocket as socket
except:
  import socket
  
from time import sleep
from machine import Pin, ADC

import network

import esp
esp.osdebug(None)

import gc
gc.collect()

pin = Pin(36, Pin.IN)
adc = ADC(pin)
adc.atten(ADC.ATTN_6DB)  # Allows up to 2.0v
adc.width(ADC.WIDTH_12BIT)  # This is the default.  Values down to 9 area allowed

ssid = 'ATC24'
password = 'Svalbard'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())
