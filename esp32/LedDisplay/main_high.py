from machine import Pin
from time import sleep

# Dictionary of temperature and led pin numbers
pin_dict = {12:13, 13:15, 14:2, 15:21, 16:23, 17:4, 18:16, 19:5, 20:18, 21:17, 22:22, 23:19, 24:32, 25:33, 26:25, 27:26, 28:27, 29:14, 30:12}

# Dictionary of temperature and led pin objects
led_dict = {}
for t,p in pin_dict.items():
    Pin(p, Pin.OUT).value(0)
    led_dict[t] = Pin(p, Pin.OUT)
    

def set_all(value):
    for t, l in led_dict.items():
        l.value(value)

    
def test_leds():
    # Function to test the leds. Do they all work? Is the sequence right?
    
    # Turn all on
    set_all(True)
    sleep(1)

    # Turn all off
    set_all(False)
    sleep(0.5)

    # Turn on in sequence from coldest to warmest
    for i in range(12,31):
        led_dict[i].value(True)
        sleep(0.05)
    sleep(0.5)

    # Reset (all off)
    set_all(False)
    

def set_temp(temp):
    # 0 maps to Pin 19 at position 8 in pin_list
    # Above 0, light pins at and above position 8
    # Below 0, light pins at and below position 8

    for t, l in led_dict.items():
        # Positive temperature - light from 0 up to temp            
        if t <= temp:
            l.value(True)
        else:
            l.value(False)
    
def test_temp():
    
    INTERVAL = 0.1
    
    for t in range(0,-7,-1):
        sleep(INTERVAL)
        set_temp(t)

    for t in range(-7,31,1):
        sleep(INTERVAL)
        set_temp(t)

    for t in range(30,0,-1):
        sleep(INTERVAL)
        set_temp(t)


test_leds()
test_temp()

set_temp(0)