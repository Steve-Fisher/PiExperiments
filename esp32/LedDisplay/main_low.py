from machine import Pin
from time import sleep
import usocket

API_READ_INTERVAL = 60  # Seconds

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

def tests():
    # Test the leds.  Do they all work?  Is the sequence right?

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
      

    # Show off cascading the leds up and down
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

    # Reset (all off)
    set_all(False)


################################################################

def gettemp():
    
    led_dict[-7].value(True)
    
    temp_api_url = '192.168.0.192'
    temp_api_port = 80

    socket_write_string = '''GET /api HTTP/1.0
Host: ''' + temp_api_url + '''
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Sec-GPC: 1
Cache-Control: max-age=0

'''

    ai = usocket.getaddrinfo(temp_api_url, temp_api_port, 0, usocket.SOCK_STREAM)
    ai = ai[0]

    s = usocket.socket(ai[0], ai[1], ai[2])
    s.connect(ai[-1])

    socket_write_bytes = bytes(socket_write_string, 'utf-8')

    s.write(socket_write_bytes)

    line = s.readline()
    find_string = '"temp": '

    while line != b'':
        if str(line).find(find_string) > 0:
            templine = str(line)
        line = s.readline()

    # Get just the temperature
    temp = templine[12:][:4]

    led_dict[-7].value(False)
    
    return round(float(temp))


tests()

while True:
    t = gettemp()
    set_temp(t)
    sleep(API_READ_INTERVAL)
        
