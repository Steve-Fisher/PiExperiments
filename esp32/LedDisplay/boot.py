from machine import Pin

# Note, Pins 1, 3, 5, 6-11, 14, 15 are HIGH after reboot
Pin(5, Pin.OUT).value(0)
Pin(14, Pin.OUT).value(0)
Pin(15, Pin.OUT).value(0)

########################################################

import network

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'ATC24'
password = 'Svalbard'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())