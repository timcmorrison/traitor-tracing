import socket
from _thread import *


# Thread function
# TODO: Could probably clean up repeated code, but works fine
def client_thread(client, key_list):
    # Receive key from client, perform initial check
    key = client.recv(1024)
    key = key.decode('utf-8')
    key_valid = True

    if key not in key_list:
            msg = "Key invalid"
            encoded_msg = msg.encode('utf-8')
            client.sendall(encoded_msg)
            key_valid = False
            client.close()

    # Key is in the list, so it is valid
    else:
        msg = "Key valid"
        encoded_msg = msg.encode('utf-8')
        client.sendall(encoded_msg)
        key_list[key] = key_list[key] + 1
        key_valid = True

    # Initial check is done
    # Continue checking as client phones home
    while key_valid:
        key = client.recv(1024)
        key = key.decode('utf-8')

        if key not in key_list:
            msg = "Key invalid"
            encoded_msg = msg.encode('utf-8')
            client.sendall(encoded_msg)
            key_valid = False
            client.close()

        # This value corresponds to the maximum number of uses for each key; 
        # Chose 2 for demonstration purposes (4 terminals on screen, 1 server + 3 clients)
        elif key_list[key] > 2:
            msg = "Key invalid"
            encoded_msg = msg.encode('utf-8')
            client.sendall(encoded_msg)
            key_valid = False
            del key_list[key]
            client.close()
            
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

    # ASCII art "Server" to make it easily identifiable during demo
    startup_msg = "███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗ \n██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗\n███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝\n╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗\n███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║\n╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝"
    print(startup_msg)

    # Key: license key
    # Value: count of simultaneous connections using the key
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
