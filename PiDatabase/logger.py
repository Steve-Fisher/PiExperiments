import datetime, time
import json, requests
import sqlite3

DB = 'logger.db'
PRINT_MESSAGES = False

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

    if PRINT_MESSAGES:
        print('Fetched header information for logID ', logID)        
        print('api_url is ', api_url)
        print('interval_secs is ', interval_secs)

    return (api_url, interval_secs)


def read_outside_temp():
    global outside_temp_api_url
    try:
        response = requests.get(outside_temp_api_url)
        temp = json.loads(response.text)['temp']
    except:
        temp = -99

    write_value(1, temp)
    
    return

def read_house_current():
    global house_current_api_url
    try:
        response = requests.get(house_current_api_url)
        v = response.text
    except:
        v = -1
    
    write_value(2, v)
    
    return 

def write_value(logID, value):
    conn = open_connection()

    # Insert value
    sql = '''INSERT INTO log(DateTimeStamp, LogID, [Value]) VALUES(datetime('now'), ?, ?);'''

    cur = conn.cursor()
    cur.execute(sql, (logID, value))

    conn.commit()
    conn.close()

    if PRINT_MESSAGES:
        print('Writen values: logID=', logID, ', value=', value)
    
    return

########################################################################################

outside_temp_api_url, outside_temp_interval_secs = get_log_header(1)
house_current_api_url, house_current_interval_secs = get_log_header(2)
outside_temp_next_read = datetime.datetime.now()
house_current_next_read = datetime.datetime.now()
counter = 0

while True:
    
    n = datetime.datetime.now()

    print("Loop iteration " + str(counter), end="\r")

    if n >= outside_temp_next_read:
        read_outside_temp()
        outside_temp_next_read = n + datetime.timedelta(seconds=outside_temp_interval_secs)

    if n >= house_current_next_read:
        read_house_current()
        house_current_next_read = n + datetime.timedelta(seconds=house_current_interval_secs)
        
    time.sleep(5)
    counter += 1