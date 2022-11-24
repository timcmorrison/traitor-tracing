import socket
import time
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: client.py key")
        exit()

    # Connect to server
    host = '127.0.0.1'
    port = 12345 # Doesn't matter, as long as it matches server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host, port))

    key = sys.argv[1]
    encoded_key = key.encode('utf-8')

    while True:
        # Send key
        server.sendall(encoded_key)

        # Wait for response
        server_responded = False
        while not server_responded:
            server_msg = server.recv(1024)
            if len(server_msg) > 1:
                server_responded = True

        # See if key was accepted
        server_msg = server_msg.decode('utf-8')
        print(server_msg)
        if "invalid" in server_msg:
            exit()

        # Else, the key was valid, so allow the user to continue
        time.sleep(5)


if __name__ == '__main__':
    main()     
