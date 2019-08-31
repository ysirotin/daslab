# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 15:19:35 2019

@author: Yevgeniy

Receive a TCP message
"""

import logging
import socket
import select
from threading import Thread
from threading import Event

class ServerThread(Thread):
    def __init__(self, host, port, callback, msgsize, logger = None):
        # initialize class variables
        self._host = host
        self._port = port
        self._callback = callback
        self._msgsize = msgsize
        self._logger = logger or logging.getLogger(self.__class__.__name__)
        self._stop_event = Event()
        
        Thread.__init__(self)
        self._logger.debug('thread initialized')
        
    def _open_socket(self):
        # open a socket for the thread to use
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setblocking(0)    
        self._sock.bind((self._host, self._port))
        self._sock.listen()

    def _close_socket(self):
        # close the socket for the thread to use
        self._sock.close()

    def run(self):
        # the main run function for the thread (runs in a loop)
        self._logger.debug('thread started')
        
        self._open_socket()
        
        inputs = [self._sock]
        outputs = []
        
        while inputs and not self._stop_event.isSet():
            readable, writeable, errored = select.select(inputs, outputs, inputs, 1)
            for item in readable:
                if item is self._sock:  # server ready to connect
                    conn, addr = self._sock.accept()
                    conn.setblocking(0)
                    inputs.append(conn)
                else:                    # incoming connection has data
                    data = item.recv(self._msgsize) 
                    self._callback(data)
                    inputs.remove(item)
                    item.close()
                    
        self._close_socket()
        self._logger.debug('thread stopped')

    def stop(self):
        # the function to stop the thread run() loop
        self._stop_event.set()

class ServerSocket:
    def __init__(self, host = None, port = 55513, callback = None, msgsize = 1024, logger = None):
        # initialize class variables
        self._thread = None
        self._callback = callback or self.default_callback
        
        self._host = host or socket.gethostbyname(socket.gethostname())
        self._port = port
        self._msgsize = msgsize
        
        self._logger = logger or logging.getLogger(self.__class__.__name__)
        
    def default_callback(self, data):
        # dummy default callback
        self._logger.info('Received: %s', str(data))
        
    def start(self, callback = None):
        # start the server thread with specified callback (default if none)
        if callback:
            self._callback = callback

        self._logger.debug('starting thread')
        self._thread = ServerThread(self._host, self._port, self._callback, self._msgsize, self._logger)
        self._thread.start()
        
    def stop(self):
        # stop the server thread
        self._logger.debug('stopping thread')
        self._thread.stop()
        self._thread.join()
        self._thread = None
        self._logger.debug('thread joined')