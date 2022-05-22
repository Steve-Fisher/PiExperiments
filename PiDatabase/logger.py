import time
import json, requests

TEMP_API_URL = 'http://192.168.0.124/api'

READ_INTERVAL = 5 # seconds

f = open('templog_' + time.strftime('%Y%m%d%H%M%S', time.localtime()) + '.txt', 'a')
f.write('Time,Outside\n')
f.flush()

read_counter = 0
last_outside_temp = 12.0

def get_outside_temp():
    global last_outside_temp
    try:
        response = requests.get(TEMP_API_URL)
        temp = json.loads(response.text)['temp']
    except:
        temp = last_outside_temp        
    finally:
        last_outside_temp = temp
    return temp

while True:
    
    print('read_counter = ' + str(read_counter), end='\r')
    
    t = get_outside_temp()
    
    f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    f.write(',' + "{:0.1f}".format(t))
    f.write('\n')
    f.flush()

    read_counter += 1
    
    time.sleep(READ_INTERVAL)