# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 15:19:35 2019

@author: Yevgeniy

Draw a stimulus upon receipt of TCP message
"""

import socket
from psychopy import visual, core, event #import some libraries from PsychoPy

# %% Global variables

HOST = socket.gethostbyname(socket.gethostname())  # get host name automatically
PORT = 55513              # Port to listen on (non-privileged ports are > 1023)

# %% Initiate Psychopy Objects
#create a psychopy window
mywin = visual.Window([800,600],monitor="testMonitor", units="deg")

#create some stimuli
grating = visual.GratingStim(win=mywin, mask='circle', size=3, pos=[-4,0], sf=3)
fixation = visual.GratingStim(win=mywin, size=0.2, pos=[0,0], sf=0, rgb=-1)

def GrtR():
    for i in range(100): #100 steps
        grating.setPhase(0.05, '+')#advance phase by 0.05 of a cycle
        grating.draw()
        fixation.draw()
        mywin.flip()
    
def GrtL():
    for i in range(100): #100 steps
        grating.setPhase(0.05, '-')#advance phase by 0.05 of a cycle
        grating.draw()
        fixation.draw()
        mywin.flip()

# %% Main program loop    

socket.setdefaulttimeout(None)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#with socket.socket(socket.AF_INET, socket.SOCK_STREAM| socket.SOCK_NONBLOCK) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    
    with conn:
        print('Connected by', addr)
        
        Flag = True
        while Flag:
            s.setblocking(0)
            TCPdata = conn.recv(1024)
            print('TCP in', TCPdata)
            thisKey=event.getKeys()
            print('Keystroke ',thisKey)
            if (thisKey in ['l', 'left'] ) or (TCPdata in [b'l', b'L']):
                GrtL()
            elif (thisKey in ['r', 'right'] ) or (TCPdata in [b'r', b'R']):
                GrtR()            
            elif (thisKey in ['q', 'escape'] ) or (TCPdata in [b'q', b'Q']):
                Flag = False
            else: 
                print("NOT RECOGNIZED")
            event.clearEvents()  # clear other (eg mouse) events - they clog the buffer
        core.wait(0.1)
                
s.close()

core.quit()



