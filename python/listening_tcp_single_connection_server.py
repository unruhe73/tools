#!/usr/bin/env python3

# TCP socket connection server with single connection on port 10'000
# it's not for multi client connection, the first client connection is served

import socket
import time
import sys
import string
from datetime import datetime

port = 10000

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('0.0.0.0', port)
print('starting server on port %s...' % server_address[1])

binded = False
while not binded:
    try:
        sock.bind(server_address)
        binded = True
    except socket.error:
        print('*** server: cannot bind on port %s, trying bind again in 5 seconds...' %  server_address[1])

        try:
            time.sleep(5)
        except KeyboardInterrupt:
            print("\nBye!")
            sys.exit(1)


# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print(f'waiting for a connection on port {server_address[1]}...')

    try:
        connection, client_address = sock.accept()
        print(f'got connection from IP {client_address[0]} on port {client_address[1]}')
        data = f"Hello there, here it is {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}\nBye!\n"
        connection.sendall(data.encode('utf-8'))
        connection.close()
    except KeyboardInterrupt:
        print("\nBye!")
        sys.exit(1)