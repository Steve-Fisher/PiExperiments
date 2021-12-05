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
TEMP_SENSORY_DEVICE_4 = '28-01204d165394' # Room

TEMP_SCALE = 'C'
BASE_TIME = time.time()

TEMP_LIMIT = 18
READ_INTERVAL = 60
CALL_COUNT_LIMIT = 5

ts1 = devices.TempSensor(TEMP_SENSORY_DEVICE_1, TEMP_SCALE)
ts2 = devices.TempSensor(TEMP_SENSORY_DEVICE_2, TEMP_SCALE)
ts3 = devices.TempSensor(TEMP_SENSORY_DEVICE_3, TEMP_SCALE)
ts4 = devices.TempSensor(TEMP_SENSORY_DEVICE_4, TEMP_SCALE)
relay1 = devices.Relay(RELAY_PIN)
call_count = 0

relay1.open(True)
relay1.open(False)

f = open('datalog' + str(BASE_TIME) + '.txt', 'a')
f.write('Time,Outside,Flow,Return,Room,Call\n')

while True:
    t_outside = ts1.read_temp()
    t_flow = ts2.read_temp()
    t_return = ts3.read_temp()
    t_room = ts4.read_temp()
    call = int(t_room < TEMP_LIMIT)
    call_count = (call_count + call)*call
    print(str(t_outside) + ' | ' + str(t_flow) + ' | ' + str(t_return) + ' | ' + str(t_room) + ' | ' + str(call_count))
    
    f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    f.write(',' + "{:0.1f}".format(t_outside))
    f.write(',' + "{:0.1f}".format(t_flow))
    f.write(',' + "{:0.1f}".format(t_return))
    f.write(',' + "{:0.1f}".format(t_room))
    f.write(',' + "{:0.0f}".format(call_count))
    f.write('\n')
    f.flush()
    
    relay1.open(call_count > CALL_COUNT_LIMIT)
    
    time.sleep(READ_INTERVAL)
    
