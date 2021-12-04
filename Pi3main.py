import devices
import time

#import glob
#base_dir = '/sys/bus/w1/devices/'
#device_id = glob.glob(base_dir + '28*')[0]
#print(device_id)

RELAY_PIN = 17
TEMP_SENSORY_DEVICE_1 = '28-3c01e07644fc' # Outside
TEMP_SENSORY_DEVICE_2 = '28-01204d205a25' # Flow
TEMP_SENSORY_DEVICE_3 = '28-01204d08a566' # Return

TEMP_SCALE = 'C'
BASE_TIME = time.time()


temp_limit = 26
read_interval = 60

ts1 = devices.TempSensor(TEMP_SENSORY_DEVICE_1, TEMP_SCALE)
ts2 = devices.TempSensor(TEMP_SENSORY_DEVICE_2, TEMP_SCALE)
ts3 = devices.TempSensor(TEMP_SENSORY_DEVICE_3, TEMP_SCALE)
relay1 = devices.Relay(RELAY_PIN)

f = open('datalog' + str(BASE_TIME) + '.txt', 'a')
f.write('Time,Outside,Flow,Return\n')

while True:
    t_outside = ts1.read_temp()
    t_flow = ts2.read_temp()
    t_return = ts3.read_temp()
    print(str(t_outside) + ' | ' + str(t_flow) + ' | ' + str(t_return))
    
    f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    f.write(',' + "{:0.1f}".format(t_outside))
    f.write(',' + "{:0.1f}".format(t_flow))
    f.write(',' + "{:0.1f}".format(t_return))
    f.write('\n')
    f.flush()
    
    #relay1.open(t3>t2)
    time.sleep(read_interval)
    
