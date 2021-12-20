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
READ_INTERVAL = 30 # seconds
RECORD_INTERVAL = 60*5 # 5 minutes
OUTSIDE_TEMP_ROLLING_AVG = 60*60*6 # 6 hours
RELAY_CYCLE_INTERVAL_LIMIT = 60*30  # 30 minutes

ts_outside = devices.TempSensor(TEMP_SENSORY_OUTSIDE_ID, TEMP_SCALE)
ts_flow    = devices.TempSensor(TEMP_SENSORY_FLOW_ID   , TEMP_SCALE)
ts_return  = devices.TempSensor(TEMP_SENSORY_RETURN_ID , TEMP_SCALE)
ts_room    = devices.TempSensor(TEMP_SENSORY_ROOM_ID   , TEMP_SCALE)
relay_heat = devices.Relay(RELAY_PIN)

# Cycle relay to ensure it starts out closed
relay_heat.open(True)
relay_heat.open(False)

f = open('datalog_' + time.strftime('%Y%m%d%H%M%S', time.localtime()) + '.txt', 'a')
f.write('Time,Outside,Flow,Return,Room,RollingAvgOutside,SlabTarget,SlabTrigger,SlabModelled,records_since_relay_change,heat_off_slab_temp,Call\n')
f.flush()

t_outside_cum = t_flow_cum = t_return_cum = t_room_cum = 0
read_counter = 0
record_counter = 0
t_outside_list = []
records_since_relay_change = 0
heat_off_slab_temp = ts_return.read_temp()
relay_state = False

while True:
    
    print('read_counter = ' + str(read_counter) + ' | record_counter = ' + str(record_counter), end='\r')
    
    t_outside_cum += ts_outside.read_temp()
    t_flow_cum    += ts_flow.read_temp()
    t_return_cum  += ts_return.read_temp()
    t_room_cum    += ts_room.read_temp()
    read_counter += 1
    
    time.sleep(READ_INTERVAL)
    
    if read_counter*READ_INTERVAL >= RECORD_INTERVAL:
        
        t_outside_avg = t_outside_cum / read_counter
        t_flow_avg    = t_flow_cum    / read_counter
        t_return_avg  = t_return_cum  / read_counter
        t_room_avg    = t_room_cum    / read_counter
        
        # Rolling average outside temperature
        t_outside_list.append(t_outside_avg)
        while len(t_outside_list) > (OUTSIDE_TEMP_ROLLING_AVG / RECORD_INTERVAL):
            t_outside_list = t_outside_list[1:]
        t_outside_rolling_avg = sum(t_outside_list) / len(t_outside_list)
        
        # Slab target and trigger temps
        slab_target_temp = 25 - (2*t_outside_rolling_avg/5)
        slab_trigger_temp = slab_target_temp - 3
        
        # Modelled slab temperature
        x = records_since_relay_change*RECORD_INTERVAL/(60*15)  # Modelled in 15 minute intervals
        modelled_slab_temp = x*x*0.0092 - x*0.5143 + heat_off_slab_temp
        
        # Enough time has elapsed since the last relay state change
        if records_since_relay_change*RECORD_INTERVAL > RELAY_CYCLE_INTERVAL_LIMIT:
            
            # Condition to call for heat
            if t_room_avg < TEMP_LIMIT or (relay_state == False and modelled_slab_temp < slab_trigger_temp):
                if relay_state == False:
                    relay_state = True
                    records_since_relay_change = -1
                    
            # Condition to turn off heat
            if t_flow_avg > slab_target_temp:
                if relay_state == True:
                    relay_state = False
                    records_since_relay_change = -1
                    heat_off_slab_temp = t_return_avg
            
            relay_heat.open(relay_state)
            
            
        f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        f.write(',' + "{:0.1f}".format(t_outside_avg))
        f.write(',' + "{:0.1f}".format(t_flow_avg))
        f.write(',' + "{:0.1f}".format(t_return_avg))
        f.write(',' + "{:0.1f}".format(t_room_avg))
        f.write(',' + "{:0.1f}".format(t_outside_rolling_avg))
        f.write(',' + "{:0.1f}".format(slab_target_temp))
        f.write(',' + "{:0.1f}".format(slab_trigger_temp))
        f.write(',' + "{:0.1f}".format(modelled_slab_temp))
        f.write(',' + "{:0.0f}".format(records_since_relay_change))
        f.write(',' + "{:0.1f}".format(heat_off_slab_temp))
        f.write(',' + "{:0.0f}".format(relay_state))
        f.write('\n')
        f.flush()
        record_counter += 1
        
        t_outside_cum = t_flow_cum = t_return_cum = t_room_cum = 0
        read_counter = 0
        records_since_relay_change += 1
