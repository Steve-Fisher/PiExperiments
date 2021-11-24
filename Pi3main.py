import devices
import time

#import glob
#base_dir = '/sys/bus/w1/devices/'
#device_id = glob.glob(base_dir + '28*')[0]
#print(device_id)

RELAY_PIN = 17
TEMP_SENSORY_DEVICE = '28-000000038dbb'
TEMP_SCALE = 'C'

temp_limit = 26
read_interval = 1

ts1 = devices.TempSensor(TEMP_SENSORY_DEVICE, TEMP_SCALE)
relay1 = devices.Relay(RELAY_PIN)

while True:
    temp = ts1.read_temp()
    print(temp)
    relay1.open(temp>temp_limit)
    time.sleep(read_interval)
    
