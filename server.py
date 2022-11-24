import socket

# Start server, listen for connections
host = '' # Symbolic name meaning all available interfaces
port = 12345 # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)

# If client tries connecting, check if key is valid
key_list = []
key_list.append("veryvalidkey")

while True:
    conn, addr = s.accept()
    print('Connected by', addr)

    key = conn.recv(1024)
    key = key.decode('utf-8')
    key_valid = True

    if key not in key_list:
        key_valid = False
        msg = "Your key is not valid, try buying one bozo ;)"
        encoded_msg = msg.encode('utf-8')
        conn.sendall(encoded_msg)
    else:
        msg = "Your key is valid, thanks for being a totally legit paying customer"
        encoded_msg = msg.encode('utf-8')
        conn.sendall(encoded_msg)

    while key_valid:
        data = conn.recv(1024)
        if not data: break
        conn.sendall(data)
    conn.close()
