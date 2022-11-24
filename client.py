from http import server
import socket
from wsgiref.simple_server import server_version

# Connect to server
host = socket.gethostname()
port = 12345 # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

# Send key
key = "veryvalidkey"
encoded_key = key.encode('utf-8')
s.sendall(encoded_key)

# Wait for response
server_response = False
while not server_response:
    data = s.recv(1024)
    if len(data) > 1:
        server_response = True

s.close()
print('Received', repr(data)[1:])