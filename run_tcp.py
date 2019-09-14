# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 16:51:56 2019

@author: Yevgeniy
"""

import logging
from tcp_receive import ServerSocket
from psychopy import visual, core, event  #import some libraries from PsychoPy

def setup_logger():
    # setup basic logging       
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

if __name__ == "__main__":

    logger = setup_logger()

    #create a window
    mywin = visual.Window([800, 600], monitor="testMonitor", units="deg", gammaErrorPolicy = 'warn')

    #create some stimuli
    grating = visual.GratingStim(win=mywin, mask='circle', size=3, pos=[-4,0], sf=3)
    fixation = visual.GratingStim(win=mywin, size=0.2, pos=[0,0], sf=0, rgb=-1)

    def Grt(direction):
        # update grating phase'
        grating.setPhase(0.05, direction) #advance phase by 0.05 of a cycle
        grating.draw()
        fixation.draw()
        mywin.flip()

    def interpret_message(msg):
        # translate messages into grating directions or exit
        global run
        global direction
        if msg in ['l', 'left']:
            direction = '-'
            logger.info('grating left')
        elif msg in ['r', 'right']:
            direction = '+'
            logger.info('grating right')
        elif msg in ['q', 'escape']:
            run = False
            logger.info('quit received')
        else:
            logger.error('unknown message: %s', msg)

    def tcp_callback(data):
        # the callback function for incoming TCP data
        logger.info('Received data: %s', data.decode())
        interpret_message(data.decode().lower())

    server = ServerSocket(port=55513, callback=tcp_callback, logger=logger)
    server.start()
    logger.info('Started TCP server...')

    run = True
    direction = '+'
    while run:
        Grt(direction)
        
        core.wait(0.01)
        keys = event.getKeys()
        if len(keys):
            interpret_message(keys[0])

    server.stop()
    logger.info('Stopped server')
    mywin.close()