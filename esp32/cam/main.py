from machine import Pin
from time import sleep

ledPin = 4;

p = Pin(ledPin, Pin.OUT)

p.value(True)
sleep(1)
p.value(False)
sleep(1)

#######################################

import camera

camera.init(0, format=camera.JPEG) 
#camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)

camera.deinit()

buf = camera.capture()
print(type(buf))
