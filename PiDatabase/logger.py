import time
import json, requests
import sqlite3

DB = 'logger.db'

def open_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB)
    except sqlite3.Error as e:
        print(e)
    return conn

def get_log_header(logID):
    conn = open_connection()
    cur = conn.cursor()
    
    sql = 'SELECT API_URL, interval_secs FROM logheader WHERE logID = ' + str(logID) + ';'
    cur.execute(sql)

    row = cur.fetchall()[0]
    api_url = row[0]
    interval_secs = row[1]

    cur.close()
    conn.close()

    return (api_url, interval_secs)


def get_outside_temp(api_url):
    global last_outside_temp
    try:
        response = requests.get(api_url)
        temp = json.loads(response.text)['temp']
    except:
        temp = last_outside_temp        
    finally:
        last_outside_temp = temp
    return temp

def write_value(logID, value):
    conn = open_connection()

    # Insert value
    sql = '''INSERT INTO log(DateTimeStamp, LogID, [Value]) VALUES(datetime('now'), ?, ?);'''

    cur = conn.cursor()
    cur.execute(sql, (logID, value))

    conn.commit()
    conn.close()

########################################################################################

api_url, interval_secs = get_log_header(1)
read_counter = 0

while True:
    
    print('read_counter = ' + str(read_counter), end='\r')
    
    t = get_outside_temp(api_url)
    
    write_value(1, t)

    read_counter += 1
    time.sleep(interval_secs)