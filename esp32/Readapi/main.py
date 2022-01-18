import usocket

def gettemp():
    
    temp_api_url = '192.168.0.192'
    temp_api_port = 80

    socket_write_string = '''GET /api HTTP/1.0
Host: ''' + temp_api_url + '''
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Sec-GPC: 1
Cache-Control: max-age=0

'''

    ai = usocket.getaddrinfo(temp_api_url, temp_api_port, 0, usocket.SOCK_STREAM)
    ai = ai[0]

    s = usocket.socket(ai[0], ai[1], ai[2])
    s.connect(ai[-1])

    socket_write_bytes = bytes(socket_write_string, 'utf-8')

    s.write(socket_write_bytes)

    line = s.readline()
    find_string = '"temp": '

    while line != b'':
        if str(line).find(find_string) > 0:
            templine = str(line)
        line = s.readline()

    # Get just the temperature
    temp = templine[12:][:4]

    return temp


print(gettemp())