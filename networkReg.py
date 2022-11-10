import colorsys
import contextlib # used to supress pygame hello message
import math
import multiprocessing as mp
import random
import socket
import struct
import sys
import time

with contextlib.redirect_stdout(None): # suppresses pygame hello message
    import pygame
    
from donut import *  # the donut file

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

def receive(MCAST_GRP, MCAST_PORT, IS_ALL_GROUPS, flagStop):
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
            flagStop.set()
            time.sleep(5)
            flagStop.clear()
            # needs to stop instead of just printing uh oh. Should probably stop for 5 seconds since that's how often signal is sent.
            # might get messed up if more 3+ duplicates are running






def main():
    key = '0034' # key for product
    flagStop = mp.Event() # flag for when to stop



    if len(sys.argv) != 2:
        return 0
    if sys.argv[1] == key:
        print("correct key detected")
        # sets up threading
        sender = mp.Process(target=send, args=(MCAST_GRP, MCAST_PORT))
        receiver = mp.Process(target=receive, args=(MCAST_GRP, MCAST_PORT, IS_ALL_GROUPS, flagStop))
        #spinner = mp.Process(target = donut.runDonut())

        # begins threading
        sender.start()
        receiver.start()
        #spinner.start()

        #donut stuff go here
        global A, B, x_start, y_start, hue, screen
        run = True
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
        while run:

            screen.fill((black))

            z = [0] * screen_size  # Donut. Fills donut space
            b = [' '] * screen_size  # Background. Fills empty space

            for j in range(0, 628, theta_spacing):  # from 0 to 2pi
                for i in range(0, 628, phi_spacing):  # from 0 to 2pi
                    c = math.sin(i)
                    d = math.cos(j)
                    e = math.sin(A)
                    f = math.sin(j)
                    g = math.cos(A)
                    h = d + 2
                    D = 1 / (c * h * e + f * g + 5)
                    l = math.cos(i)
                    m = math.cos(B)
                    n = math.sin(B)
                    t = c * h * g - f * e
                    x = int(x_offset + 40 * D * (l * h * m - t * n))  # 3D x coordinate after rotation
                    y = int(y_offset + 20 * D * (l * h * n + t * m))  # 3D y coordinate after rotation
                    o = int(x + columns * y)  
                    N = int(8 * ((f * e - c * d * g) * m - c * d * e - f * g - l * d * n))  # luminance index
                    if rows > y and y > 0 and x > 0 and columns > x and D > z[o]:
                        z[o] = D
                        b[o] = chars[N if N > 0 else 0]

            if y_start == rows * y_separator - y_separator:
                y_start = 0

            for i in range(len(b)):
                A += random.uniform(0, 0.0001)  # for faster rotation change to bigger value
                B += random.uniform(0, 0.0001)  # for faster rotation change to bigger value
                if i == 0 or i % columns:
                    text_display(b[i], x_start, y_start, display_surface)
                    x_start += x_separator
                else:
                    y_start += y_separator
                    x_start = 0
                    text_display(b[i], x_start, y_start, display_surface)
                    x_start += x_separator

            #print(flagStop.is_set())
            while flagStop.is_set():
                time.sleep(5)

            pygame.display.update()

            hue += 0.005

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

if __name__ == "__main__":
    main()