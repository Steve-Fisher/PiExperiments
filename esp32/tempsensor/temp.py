try:
  import usocket as socket
except:
  import socket
  
from time import sleep
from machine import Pin
import onewire, ds18x20

import network

import esp
esp.osdebug(None)

import gc
gc.collect()

ds_pin = Pin(4)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

ssid = 'ATC24'
password = 'Svalbard'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

########################################################

def read_ds_sensor():
  #roms = ds_sensor.scan()
  #print('Found DS devices: ', roms)
  #for rom in roms:
  #rom = bytearray(b'(\xb0\x18\x0bM \x01q')  #roms[0]
  rom = bytearray(b'(\xfcDv\xe0\x01<X')
  ds_sensor.convert_temp()
  temp = ds_sensor.read_temp(rom)
  if isinstance(temp, float):
    msg = round(temp, 1)
    print(temp, end=' ')
    print('Valid temperature')
    return msg
  return b'0.0'
  
def web_page():
  temp = read_ds_sensor()
  html = """<!DOCTYPE HTML><html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style> html { font-family: Arial; display: inline-block; margin: 0px auto; text-align: center; }
    h2 { font-size: 3.0rem; } p { font-size: 3.0rem; } .units { font-size: 1.2rem; } 
  </style>
</head>
<body><h2>Outside Temperature</h2>
  <p>
    <span id="temperature">""" + str(temp) + """&deg;C</span>
  </p>
</body>
</html>"""
  return html

def api_response():
  temp = read_ds_sensor()
  json = """{
  "temp": """ + str(temp) + """
}"""
  return bytes(json, 'utf-8')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  try:
    if gc.mem_free() < 102000:
      gc.collect()
    conn, addr = s.accept()
    conn.settimeout(3.0)
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    conn.settimeout(None)
    request = str(request)
    print('Content = %s' % request)
    f = request[request.find('GET /') + 5:request.find(' HTTP/')]
    conn.send('HTTP/1.0 200 OK\n')
    if f == 'api':
        response = api_response()
        conn.send('Content-Type: application/json\n')
    else:
        response = web_page()
        conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
    print('Sent response %s' % response)
  except OSError as e:
    conn.close()
    print('Connection closed')
