import tempsensor as ts
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
relay = 17
temp_limit = 26

relay_on = True
GPIO.setup(relay, GPIO.OUT) # GPIO Assign mode

while True:
    t = ts.read_temp()
    print(t)
    if relay_on and (t>temp_limit):
        GPIO.cleanup(relay)
        relay_on = False
    if not(relay_on) and (t<temp_limit):
        GPIO.setup(relay, GPIO.OUT) # GPIO Assign mode
        relay_on = True
    time.sleep(1)
    
