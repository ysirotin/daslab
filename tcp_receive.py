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
    def __init__(self, sock, callback, msgsize, logger = None):
        self._sock = sock
        self._callback = callback
        self._msgsize = msgsize
        self._logger = logger or logging.getLogger(self.__class__.__name__)
        self._stop_event = Event()
        
        Thread.__init__(self)
        self._logger.debug('thread initialized')
        
    def run(self):
        self._logger.debug('thread started')
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
                    
        self._logger.debug('thread stopped')

    def stop(self):
        self._stop_event.set()

class ServerSocket:
    def __init__(self, port = 55513, callback = None, msgsize = 1024, logger = None):
        self._thread = None
        self._callback = callback or self.default_callback
        
        self._host = socket.gethostbyname(socket.gethostname())
        self._port = port
        self._msgsize = msgsize
        
        self._logger = logger or logging.getLogger(self.__class__.__name__)
    
    def _open_socket(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setblocking(0)    
        self._sock.bind((self._host, self._port))
        self._sock.listen()

    def _close_socket(self):
        self._sock.close()
    
    def default_callback(self, data):
        self._logger.info('Received: %s', str(data))
        
    def start(self, callback = None):
        if callback:
            self._callback = callback
        self._open_socket()
        self._logger.debug('starting thread')
        self._thread = ServerThread(self._sock, self._callback, self._msgsize, self._logger)
        self._thread.start()
        
    def stop(self):
        self._logger.debug('stopping thread')
        self._thread.stop()
        self._thread.join()
        self._thread = None
        self._logger.debug('thread joined')
        self._close_socket()
        
