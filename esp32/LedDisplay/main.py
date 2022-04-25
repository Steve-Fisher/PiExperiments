from machine import Pin
from time import sleep
import usocket
import params_common as pc
import params_specific as ps

last_temp = pc.DEFAULT_TEMP
min_temp = 99
max_temp = -99

# Dictionary of temperature and led pin objects
led_dict = {}
for t,p in ps.PIN_DICT.items():
    Pin(p, Pin.OUT).value(0)
    led_dict[t] = Pin(p, Pin.OUT)
    if t < min_temp:
        min_temp = t
    if t > max_temp:
        max_temp = t
    

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

    # All on off test
    set_all(True)
    sleep(1)
    set_all(False)

    if pc.SEQUENCE_TEST == True:
        # Turn on in sequence from coldest to warmest
        for i in range(min_temp, max_temp+1):
            led_dict[i].value(True)
            sleep(0.05)
        sleep(0.5)

        # Reset (all off)
        set_all(False)
      

    if pc.CASCADE_TEST == True:
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
    
    global last_temp
    
    led_dict[ps.SIGNAL_LED_TEMP].value(True)
   
    try:
        t = read_temp_api()
    except:
        t = last_temp
    
    last_temp = t

    led_dict[ps.SIGNAL_LED_TEMP].value(False)
    
    return t


def read_temp_api():

    FIND_STRING = '    <span id="temperature">'
    END_STRING = '&deg;C</span>'

    try:
        proto, dummy, host, path = pc.TEMP_API_URL.split("/", 3)
    except ValueError:
        proto, dummy, host = pc.TEMP_API_URL.split("/", 2)
        path = ""
    if proto == "http:":
        port = 80
    else:
        raise ValueError("Unsupported protocol: " + proto)

    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)
    
    ai = usocket.getaddrinfo(host, port, 0, usocket.SOCK_STREAM)
    ai = ai[0]
    
    r = b''
    e = 0
    
    while r == b'':
        
        try:
            s = usocket.socket(ai[0], ai[1], ai[2])
            s.connect(ai[-1])
            
            s.write(b"GET /")
            s.write(path)
            s.write(b" HTTP/1.0\r\nHost: ")
            s.write(host)
            s.write(b"\r\n")

            r = s.read()

            s.close()

        except OSError:
            e += 1
            sleep(1)
            if e == 10:
                raise
            
    r = r.decode('UTF-8')
    temp = r[r.find(pc.FIND_STRING)+len(pc.FIND_STRING):r.rfind(pc.END_STRING)]

    return round(float(temp))


tests()

while True:
    t = gettemp()
    set_temp(t)
    sleep(pc.API_READ_INTERVAL)
        