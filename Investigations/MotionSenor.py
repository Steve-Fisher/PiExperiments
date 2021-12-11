import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
pir = 17

GPIO.setup(pir, GPIO.IN)

print('Waiting for sensor to settle')
time.sleep(2)
m = 0

print('Detecting motion')

while True:
    if GPIO.input(pir): #Check whether pir is HIGH
        m += 1
        print(str(m) + ' - Motion Detected!')
        time.sleep(2) #D1- Delay to avoid multiple detection
    time.sleep(0.1) #While loop delay should be less than detection(hardware) delay
