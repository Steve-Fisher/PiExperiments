from machine import Pin
from ds18x20 import DS18X20
from onewire import OneWire
import time

SAMPLE_INTERVAL = 60 # in seconds

#Initialize the onboard LED as output
led = Pin(25, Pin.OUT)
led.value(0)

def dtstr(t):
    return '{:02d}{:02d}{:02d}_{:02d}{:02d}{:02d}'.format(t[0],t[1],t[2],t[3],t[4],t[5])

# Initialize DS18x20
ts1 = DS18X20(OneWire(Pin(22)))
ts2 = DS18X20(OneWire(Pin(27)))

f = open('datalog' + dtstr(time.localtime()) + '.txt', 'a')
f.write('DateTime,Temp1,Temp2\n')

while True:
    
    led.value(1)
    
    ts1.convert_temp()
    ts2.convert_temp()
    
    t1 = ts1.read_temp(ts1.scan()[0])
    t2 = ts2.read_temp(ts2.scan()[0])
    
    time.sleep_ms(200)
    
    #print(str(t1) + ' | ' + str(t2))
    
    f.write(dtstr(time.localtime()))
    f.write(',' + "{:0.1f}".format(t1))
    f.write(',' + "{:0.1f}".format(t2))
    f.write('\n')
    f.flush()

    led.value(0)
    
    time.sleep_ms(SAMPLE_INTERVAL * 1000)
    