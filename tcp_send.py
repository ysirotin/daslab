# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 15:19:35 2019

@author: Yevgeniy

Send a TCP message to host
"""

import socket
import argparse

# %% Global variables

PORT = 55513

localhost = socket.gethostbyname(socket.gethostname())

parser = argparse.ArgumentParser(description='Send some data over TCP.')
parser.add_argument('--host', '-H', type=str, help='server host', default=localhost)
parser.add_argument('--port', '-P', type=int, help='server port', default=PORT)
parser.add_argument('message', nargs = 1) 
args = parser.parse_args()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    try:
        sock.connect((args.host, args.port))
        sock.send(args.message[0].encode())
    except:
        print('Failed to send message!')
    
