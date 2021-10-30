from machine import Pin
from DHT22 import DHT22
from oled import OLED_1inch3
from ds18x20 import DS18X20
from onewire import OneWire
import time

#Initialize the onboard LED as output
led = Pin(25, Pin.OUT)

# Initialize DHT22
dht22 = DHT22(Pin(4,Pin.IN,Pin.PULL_UP))

# Initialize DS18x20
ds = DS18X20(OneWire(Pin(2)))
rom = ds.scan()[0]

# Clear display
OLED = OLED_1inch3()
OLED.fill(0x0000) 
OLED.show()


while True:
    ds.convert_temp()
    Tdx = ds.read_temp(rom)
    time.sleep_ms(200)

    T, H = dht22.read()
 
    OLED.fill(0x0000) 
    OLED.text("Temp_1: " +"{:0.1f}".format(T)+ "C",1,10,OLED.white)
    OLED.text('Temp_2: ' +"{:0.1f}".format(Tdx)+ "C",1,27,OLED.white)
    OLED.text('Humid_1: ' +"{:0.1f}".format(H)+ "%",1,44,OLED.white)  
    OLED.show()
    