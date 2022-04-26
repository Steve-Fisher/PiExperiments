ROM = bytearray(b'(\xb0\x18\x0bM \x01q')

#####################################################################################

ds_sensor.convert_temp()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

#####################################################################################

def read_ds_sensor():

  global ROM
  
  #roms = ds_sensor.scan()
  #print('Found DS devices: ', roms)
  #for rom in roms:
  #rom = bytearray(b'(\xb0\x18\x0bM \x01q')  #roms[0]

  temp = ds_sensor.read_temp(ROM)
  
  if isinstance(temp, float):
    rtn = round(temp, 1)
  else:
    rtn = -99
 
  return rtn


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

#####################################################################################

while True:
  try:
    if gc.mem_free() < 102000:
      gc.collect()
    conn, addr = s.accept()
    conn.settimeout(3.0)
#    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    conn.settimeout(None)
    request = str(request)
#    print('Content = %s' % request)
    f = request[request.find('GET /') + 5:request.find(' HTTP/')]
    conn.send('HTTP/1.0 200 OK\n')
    if f == 'api':
        conn.send('Content-Type: application/json\n')
        response = api_response()
    else:
        response = web_page()
        conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
#    print('Sent response %s' % response)
  except OSError as e:
    conn.close()
#    print('Connection closed')