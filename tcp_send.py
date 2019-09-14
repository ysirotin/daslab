# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 15:19:35 2019

@author: Yevgeniy

Send a TCP message to host
"""

import socket
import argparse
import time

# %% Global variables

PORT = 55513
TERM = b'\x00'

localhost = socket.gethostbyname(socket.gethostname())

parser = argparse.ArgumentParser(description='Send some data over TCP.')
parser.add_argument('--host', '-H', type=str, help='server host', default=localhost)
parser.add_argument('--port', '-P', type=int, help='server port', default=PORT)
parser.add_argument('--delay', '-D', type=float, help='message delay', default=0.)
parser.add_argument('message', nargs = '+')
args = parser.parse_args()

print(args.message)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    try:
        sock.connect((args.host, args.port))
        
        for message in args.message:
            # this is the data payload
            data = message.encode()
            
            # this is the header (2 bytes with message length)
            header = (len(data)).to_bytes(2, byteorder='little')
            
            sock.send(header + data)
            time.sleep(args.delay)
    except:
        print('Failed to send message!')