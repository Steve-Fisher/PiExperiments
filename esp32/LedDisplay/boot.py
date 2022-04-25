from machine import Pin
import params_network

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

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(params_network.SSID, params_network.PW)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())