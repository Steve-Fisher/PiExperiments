from machine import Pin
from time import sleep

pin_list = [23, 21, 22, 19, 18, 5, 17, 16, 15]
led_list = []

for p in pin_list:
    Pin(p, Pin.OUT).value(0)
    led_list.append(Pin(p, Pin.OUT))
    
def test_leds():
    for l in led_list:
        l.value(1)
        sleep(0.2)
        l.value(0)

def set_temp(temp):
    i = 0
    for l in led_list:
        l.value(i<=temp)
        i += 1

test_leds()

sleep(1)
set_temp(2)

sleep(1)
set_temp(5)

sleep(1)
set_temp(0)

sleep(1)
set_temp(10)

sleep(1)
set_temp(-1)