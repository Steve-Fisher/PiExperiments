'''
Pi Poller.  Calls ESP32 API and stores values
'''

import time
import json, requests

TEMP_API_URL = 'http://192.168.0.136'

READ_INTERVAL = 5 # seconds

f = open('powerlog_' + time.strftime('%Y%m%d%H%M%S', time.localtime()) + '.txt', 'a')
f.write('Time,Value\n')
f.flush()

read_counter = 0

def get_power():
    try:
        response = requests.get(TEMP_API_URL)
        v = response.text
    except:
        v = -1
    return v

while True:
    
    print('read_counter = ' + str(read_counter), end='\r')
    
    p = get_power()

    f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    f.write(',' + p)
    f.write('\n')
    f.flush()

    read_counter += 1
    
    time.sleep(READ_INTERVAL)
    
        
            
        
