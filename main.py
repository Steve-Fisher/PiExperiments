from machine import Pin
from DHT22 import DHT22
#from ePaper import EPD_2in9_B
from ds18x20 import DS18X20
from onewire import OneWire
import time

SAMPLE_INTERVAL = 60 # in seconds
BASE_TIME = time.time()

#Initialize the onboard LED as output
led = Pin(25, Pin.OUT)

# Initialize DHT22
dht22 = DHT22(Pin(4,Pin.IN,Pin.PULL_UP))

# Initialize DS18x20
ds = DS18X20(OneWire(Pin(2)))
rom = ds.scan()[0]

# Clear EPD screen
#epd = EPD_2in9_B()
#epd.Clear(0xff, 0xff)
#time.sleep_ms(5000)

f = open('datalog' + str(BASE_TIME) + '.txt', 'w')
f.write('Base time = ' + str(BASE_TIME) + '\n\n')
f.write('Seconds,DS18x20_Temp,DHT22_Temp,DHT22_Humid\n')

while True:
    
    led.toggle()
    
    ds.convert_temp()
    T1 = ds.read_temp(rom)
    
    T2, H2 = dht22.read()
   
    f.write(str(time.time()-BASE_TIME))
    f.write(',' + "{:0.1f}".format(T1))
    f.write(',' + "{:0.1f}".format(T2))
    f.write(',' + "{:0.1f}".format(H2))
    f.write('\n')
    
    led.toggle()
    
    # Wait
    time.sleep_ms(SAMPLE_INTERVAL*1000)