import socket
from _thread import *


# Thread function
def client_thread(client, key_list):
    # Check if key is valid
    key = client.recv(1024)
    key = key.decode('utf-8')
    key_valid = True

    if key not in key_list:
            msg = "Key invalid"
            encoded_msg = msg.encode('utf-8')
            client.sendall(encoded_msg)
            key_valid = False
    else:
        msg = "Key valid"
        encoded_msg = msg.encode('utf-8')
        client.sendall(encoded_msg)
        key_list[key] = key_list[key] + 1
    # Continue checking as client phones home
    while key_valid:
        key = client.recv(1024)
        key = key.decode('utf-8')

        if key not in key_list:
            msg = "Key invalid"
            encoded_msg = msg.encode('utf-8')
            client.sendall(encoded_msg)
            key_valid = False
        # This value corresponds to the maximum number of uses for each key; 
        # Arbitrarily chose 2
        elif key_list[key] > 2:
            msg = "Key invalid"
            encoded_msg = msg.encode('utf-8')
            client.sendall(encoded_msg)
            key_valid = False
        else:
            msg = "Key valid"
            encoded_msg = msg.encode('utf-8')
            client.sendall(encoded_msg)

def main():
    # Start server, listen for connections on an arbitrary port
    host = ""
    port = 12345
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(3)

    # Key: license key; Value: count of simultaneous connections using the key
    key_list = {}
    key_list["veryvalidkey"] = 0
    key_list["goodkey"] = 0

    # Loop until client decides to exit
    while True:
        client, addr = server.accept()
        print('Connected by', addr)
        start_new_thread(client_thread, (client,key_list))


if __name__ == '__main__':
    main()      
