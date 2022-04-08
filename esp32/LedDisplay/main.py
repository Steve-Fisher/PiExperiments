from machine import Pin
from time import sleep

pin_list = [2, 4, 17, 16, 15, 5, 18]

led_list = []

for p in pin_list:
    Pin(p, Pin.OUT).value(0)
    led_list.append(Pin(p, Pin.OUT))
    
def test_leds():
    TEST_SLEEP_INTERVAL = 0.2
    for l in led_list:
        l.value(1)
        sleep(TEST_SLEEP_INTERVAL)
        l.value(0)
    sleep(TEST_SLEEP_INTERVAL)
    
    set_temp(-1) # All off (low temp)
    sleep(TEST_SLEEP_INTERVAL)
    
    set_temp(5) # Some on, some off
    sleep(TEST_SLEEP_INTERVAL*3)
    
    set_temp(-1) # All off (low temp)
    sleep(TEST_SLEEP_INTERVAL*2)
    
    set_temp(99) # All on (high temp)
    sleep(TEST_SLEEP_INTERVAL*3)
    
    set_temp(-1)  # All off for exit

def set_temp(temp):
    i = 0
    for l in led_list:
        l.value(i<=temp)
        i += 1

# Startup Test
test_leds()

#set_temp(99)