'''
 Demonstrates DS18X20 temperature sensor
'''

from machine import Pin
from ds18x20 import DS18X20
from onewire import OneWire
import time 

#Initialize the onboard LED as output
led = Pin(25, Pin.OUT)

ds = DS18X20(OneWire(Pin(2)))

rom = ds.scan()[0]

while True:
    ds.convert_temp()
    time.sleep_ms(750)
    print(str('T: ' +"{:0.1f}".format(ds.read_temp(rom))+ "C"))
    time.sleep(5)
