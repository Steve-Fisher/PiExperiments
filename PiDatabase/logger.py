import time
import json, requests
import sqlite3

TEMP_API_URL = 'http://192.168.0.124/api'
READ_INTERVAL = 5 # seconds

DB = 'logger.db'

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


def write_value(logID, value):
        
    # Open database connection
    conn = None
    try:
        conn = sqlite3.connect(DB)
    except sqlite3.Error as e:
        print(e)
        
    # Insert value
    sql = '''INSERT INTO log(DateTimeStamp, LogID, [Value]) VALUES(datetime('now'), ?, ?);'''

    cur = conn.cursor()
    cur.execute(sql, (logID, value))

    conn.commit()
    conn.close()


read_counter = 0
last_outside_temp = 12.0

while True:
    
    print('read_counter = ' + str(read_counter), end='\r')
    
    t = get_outside_temp()
    
    write_value(1, t)

    read_counter += 1
    
    time.sleep(READ_INTERVAL)