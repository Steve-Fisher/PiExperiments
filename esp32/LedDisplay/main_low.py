from machine import Pin
from time import sleep

# Dictionary of temperature and led pin numbers
pin_dict = {-7:4, -6:2, -5:15, -4:16, -3:17, -2:5, -1:18, 0:19, 1:21, 2:22, 3:23, 4:32, 5:33, 6:25, 7:26, 8:27, 9:14, 10:12, 11:13}

# Dictionary of temperature and led pin objects
led_dict = {}
for t,p in pin_dict.items():
    Pin(p, Pin.OUT).value(0)
    led_dict[t] = Pin(p, Pin.OUT)
    

def set_all(value):
    for t, l in led_dict.items():
        l.value(value)

    
def test_leds():
# Function to test the leds.  Do they all work?  Is the sequence right?
    
    # Turn all on
    set_all(True)
    sleep(1)

    # Turn all off
    set_all(False)
    sleep(0.5)

    # Turn on in sequence from coldest to warmest
    for i in range(-7,12):
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
        # Minus temperature - light from 0 down to temp
        if temp < 0 and t < 0 and t >= temp:
            l.value(True)
        # Positive temperature - light from 0 up to temp            
        elif temp > 0 and t > 0 and t <= temp:
            l.value(True)
        # Zero (freezing) - just light 0            
        elif t == 0:
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