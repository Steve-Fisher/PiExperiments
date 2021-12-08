import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers

class Relay:

    ''' JQC-2FF-S-Z 10 amp relay '''
    
    state_open = False
    
    def __init__(self, pin):
        self.pin = pin
        self.state_open = False
        
    def open(self, state):
        if not(self.state_open) and state:
            GPIO.setup(self.pin, GPIO.OUT) # GPIO Assign mode
            self.state_open = True
        if self.state_open and not(state):
            GPIO.cleanup(self.pin)
            self.state_open = False
    
    def toggle(self):
        self.open(not(self.state))


class TempSensor:
    
    ''' 1-Wire DS18B20 temperature sensor '''
    
    def __init__(self, device_id, scale):
        self.device_file = '/sys/bus/w1/devices/' + device_id + '/w1_slave'
        self.scale = scale.upper()
    
    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        
        lines = self.read_temp_raw()
        
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        
        equals_pos = lines[1].find('t=')
        
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            
            if self.scale == 'F':
                temp = float(temp_string) / 1000.0 * 9.0 / 5.0 + 32.0    
            else:
                temp = float(temp_string) / 1000.0

        return temp

