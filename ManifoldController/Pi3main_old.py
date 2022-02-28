import devices
import time

#import glob
#base_dir = '/sys/bus/w1/devices/'
#device_id = glob.glob(base_dir + '28*')[0]
#print(device_id)

RELAY_PIN = 17
TEMP_SENSORY_OUTSIDE_ID = '28-3c01e07644fc'
TEMP_SENSORY_FLOW_ID    = '28-01204d205a25'
TEMP_SENSORY_RETURN_ID  = '28-01204d08a566'
TEMP_SENSORY_ROOM_ID    = '28-01204d165394'

TEMP_SCALE = 'C'

TEMP_LIMIT = 18
READ_INTERVAL = 60 # seconds
STATE_COUNT_FOR_CHANGE = 5
ANTI_CYCLE_LIMIT = 15

ts_outside = devices.TempSensor(TEMP_SENSORY_OUTSIDE_ID, TEMP_SCALE)
ts_flow    = devices.TempSensor(TEMP_SENSORY_FLOW_ID   , TEMP_SCALE)
ts_return  = devices.TempSensor(TEMP_SENSORY_RETURN_ID , TEMP_SCALE)
ts_room    = devices.TempSensor(TEMP_SENSORY_ROOM_ID   , TEMP_SCALE)
relay_heat = devices.Relay(RELAY_PIN)

# Cycle relay to ensure it starts out closed
relay_heat.open(True)
relay_heat.open(False)

f = open('datalog_' + time.strftime('%Y%m%d%H%M%S', time.localtime()) + '.txt', 'a')
f.write('Time,Outside,Flow,Return,Room,Call\n')

first_loop = True

while True:
    
    t_outside = ts_outside.read_temp()
    t_flow    = ts_flow.read_temp()
    t_return  = ts_return.read_temp()
    t_room    = ts_room.read_temp()
    
    below_target_temp = int(t_room < TEMP_LIMIT)
    
    if first_loop:
    
        relay_heat_state = below_target_temp
        relay_heat.open(relay_heat_state)
        count_since_last_relay_change = 0
        same_below_target_temp_state_count = 0
        first_loop = False
    
    else:
        
        count_since_last_relay_change += 1
        
        if (below_target_temp == last_below_target_temp):
            same_below_target_temp_state_count += 1
        else:
            same_below_target_temp_state_count = 0
            
        if (same_below_target_temp_state_count >= STATE_COUNT_FOR_CHANGE) and (count_since_last_relay_change >= ANTI_CYCLE_LIMIT):
            relay_heat_state = below_target_temp
            relay_heat.open(relay_heat_state)
            count_since_last_relay_change = 0
            
    print(str(t_outside) + ' | ' + str(t_flow) + ' | ' + str(t_return) + ' | ' + str(t_room) + ' | ' + str(relay_heat_state))
    
    f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    f.write(',' + "{:0.1f}".format(t_outside))
    f.write(',' + "{:0.1f}".format(t_flow))
    f.write(',' + "{:0.1f}".format(t_return))
    f.write(',' + "{:0.1f}".format(t_room))
    f.write(',' + "{:0.0f}".format(relay_heat_state))
    f.write('\n')
    f.flush()
    
    time.sleep(READ_INTERVAL)
    
    last_below_target_temp = below_target_temp
