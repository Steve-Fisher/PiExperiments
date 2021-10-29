from machine import Pin
from DHT22 import DHT22
from ePaper import EPD_2in9_B
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

# Clear EPD screen
epd = EPD_2in9_B()
epd.Clear(0xff, 0xff)
time.sleep_ms(5000)

f = open('datalog1.txt', 'w')
f.write('Datetime,DHT22_Temp,DHT22_Humid,DS18x20_Temp\n')

while True:
    ds.convert_temp()
    Tdx = ds.read_temp(rom)
    
    T, H = dht22.read()
    
    #Write Humidity value. Convert the humidity into two decimal places.
    #print(str('H: ' +"{:0.1f}".format(H)+ "%"), str('T: ' +"{:0.1f}".format(T)+ "C"))
    epd.imageblack.fill(0x00)
    epd.imagered.fill(0xff)
    epd.imageblack.text(str('Temp_1: ' +"{:0.1f}".format(T)+ "C"), 0, 60, 0xff)
    epd.imageblack.text(str('Temp_2: ' +"{:0.1f}".format(Tdx)+ "C"), 0, 80, 0xff)
    epd.imageblack.text(str('Humid_1: ' +"{:0.1f}".format(H)+ "%"), 0, 160, 0xff)
    epd.imageblack.hline(10, 120, 118, 0xff)
    
    epd.display()
    
    f.write(str(time.time()))
    f.write(',' + "{:0.1f}".format(T))
    f.write(',' + "{:0.1f}".format(H))
    f.write(',' + "{:0.1f}".format(Tdx))
    f.write('\n')
    
    
    led.toggle()
    time.sleep_ms(200)
    led.value(T>30)
    
    # Wait for Five seconds. Then proceed to collect next sensor reading.
    time.sleep_ms(1000)