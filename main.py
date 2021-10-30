from machine import Pin
from DHT22 import DHT22
from oled import OLED_1inch3
from ds18x20 import DS18X20
from onewire import OneWire
import time

SAMPLE_INTERVAL = 60 # in seconds
BASE_TIME = time.time()

#Initialize the onboard LED as output
led = Pin(25, Pin.OUT)
led.value(0)

# Initialize DHT22
dht22 = DHT22(Pin(4,Pin.IN,Pin.PULL_UP))

# Initialize DS18x20
ds = DS18X20(OneWire(Pin(2)))
#time.sleep_ms(2000)
#print(ds)
rom = ds.scan()[0]

# Clear display
OLED = OLED_1inch3()
OLED.fill(0x0000) 
OLED.show()

f = open('datalog' + str(BASE_TIME) + '.txt', 'a')
f.write('Base time = ' + str(BASE_TIME) + '\n\n')
f.write('Seconds,DS18x20_Temp,DHT22_Temp,DHT22_Humid\n')

while True:
    
    led.value(1)
    
    ds.convert_temp()
    Tdx = ds.read_temp(rom)
    time.sleep_ms(200)
    T, H = dht22.read()
    
    led.value(0)
    
    OLED.fill(0x0000) 
    OLED.text("Temp_1: " +"{:0.1f}".format(T)+ "C",1,1,OLED.white)
    OLED.text('Temp_2: ' +"{:0.1f}".format(Tdx)+ "C",1,12,OLED.white)
    OLED.text('Humid_1: ' +"{:0.1f}".format(H)+ "%",1,24,OLED.white)
    OLED.text('Time: ' + str(time.time()-BASE_TIME),1,36,OLED.white) 
    OLED.show()
    
    f.write(str(time.time()-BASE_TIME))
    f.write(',' + "{:0.1f}".format(T))
    f.write(',' + "{:0.1f}".format(Tdx))
    f.write(',' + "{:0.1f}".format(H))
    f.write('\n')
    f.flush()
    
    time.sleep_ms(SAMPLE_INTERVAL * 1000)
    