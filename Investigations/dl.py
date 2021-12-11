#!/usr/bin/python
import serial
from datetime import datetime

ser = serial.Serial('/dev/ttyAMA0', 38400)
f = open('eData.csv', 'w')

try:
    while 1:
        response = ser.readline().decode('ascii')
        z = response.split(",")
        if len(z)>=2:
            p = z[2]
            d = datetime.now()
            n = d.strftime('%Y-%m-%d %H:%M:%S')
            m = n + ',' + p
            print(z)
            f.write(m + '\n')

except KeyboardInterrupt:
    ser.close()
    f.close()