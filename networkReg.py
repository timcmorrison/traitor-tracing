import time
import socket
import struct
import threading
import random
'''
The send and receive functions are modified versions of the code found here: https://stackoverflow.com/a/1794373

'''

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
IS_ALL_GROUPS = True
id = random.randint(1, 1000000) # 1-1,000,000

def send(MCAST_GRP, MCAST_PORT):
    '''
    multicasts (i.e. broadcasts) the randomly generated id of this program over port 5007
    '''
    # regarding socket.IP_MULTICAST_TTL
    # ---------------------------------
    # for all packets sent, after two hops on the network the packet will not 
    # be re-sent/broadcast (see https://www.tldp.org/HOWTO/Multicast-HOWTO-6.html)
    MULTICAST_TTL = 2

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

    # For Python 3, change next line to 'sock.sendto(b"robot", ...' to avoid the
    # "bytes-like object is required" msg (https://stackoverflow.com/a/42612820)
    while True:
        sock.sendto(str.encode("{}".format(id)), (MCAST_GRP, MCAST_PORT))
        #sock.sendto(b"robot", (MCAST_GRP, MCAST_PORT))
        time.sleep(5)

def receive(MCAST_GRP, MCAST_PORT, IS_ALL_GROUPS):
    '''
    receives any packets sent to port 5007, and compares them with the id of this program.
    If they are not the same, then that means a copied version of this program is running
    on this network, and the program should cease functioning until duplicates are no
    longer detected.
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if IS_ALL_GROUPS:
        # on this port, receives ALL multicast groups
        sock.bind(('', MCAST_PORT))
    else:
        # on this port, listen ONLY to MCAST_GRP
        sock.bind((MCAST_GRP, MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        if int(sock.recv(10240).decode()) != id:  # another instance is running
            print("UH OH!")
            # needs to stop instead of just printing uh oh. Should probably stop for 5 seconds since that's how often signal is sent.
            # might get messed up if more 3+ duplicates are running


# sets up threading
sender = threading.Thread(target=send, args=(MCAST_GRP, MCAST_PORT))
receiver = threading.Thread(target=receive, args=(MCAST_GRP, MCAST_PORT, IS_ALL_GROUPS))

# begins threading
sender.start()
receiver.start()