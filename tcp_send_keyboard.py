# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 19:43:32 2019

@author: Yevgeniy
"""

import socket
import argparse
import msvcrt

PORT = 55513
localhost = socket.gethostbyname(socket.gethostname())

parser = argparse.ArgumentParser(description='Send some data over TCP.')
parser.add_argument('--host', '-H', type=str, help='server host', default=localhost)
parser.add_argument('--port', '-P', type=int, help='server port', default=PORT)
args = parser.parse_args()

def send_message(message):
# send a message with header
    
    # this is the data payload
    data = message.encode()
    
    # this is the header (2 bytes with message length)
    header = (len(data)).to_bytes(2, byteorder='little')
    
    sock.send(header + data)
    
run = True

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    try:
        sock.connect((args.host, args.port))
        
        while run:
           if msvcrt.kbhit():
               key = msvcrt.getch().decode()
               
               print('Sending key: ' + key)   # show the key
               
               send_message(key) # send the key to the server

               if key == 'q':
                   run = False
    except:
        print('Failed to send message!')