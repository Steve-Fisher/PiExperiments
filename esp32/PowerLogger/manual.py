from time import sleep
from machine import Pin, ADC

pin = Pin(36, Pin.IN)
adc = ADC(pin)
adc.atten(ADC.ATTN_6DB)  # Allows up to 2.0v
adc.width(ADC.WIDTH_12BIT)  # This is the default.  Values down to 9 area allowed

i = 1
l=[]
while i < 1000:
    l.append(adc.read())
    i += 1

a = sum(l)/len(l)
rms = (sum([(i-a)**2 for i in l])/len(l))**0.5

p = ((rms-33.9668) / 0.08633 ) - 70
print(p)

