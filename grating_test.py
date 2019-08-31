# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 17:10:04 2019

@author: Yevgeniy
"""

from psychopy import visual, core, event  #import some libraries from PsychoPy

if __name__ == "__main__":

    #create a window
    mywin = visual.Window([800,600],monitor="testMonitor", units="deg")
    
    #create some stimuli
    grating = visual.GratingStim(win=mywin, mask='circle', size=3, pos=[-4,0], sf=3)
    fixation = visual.GratingStim(win=mywin, size=0.2, pos=[0,0], sf=0, rgb=-1)
    
    def Grt(direction):
        for i in range(100): #100 steps
            grating.setPhase(0.05, direction) #advance phase by 0.05 of a cycle
            grating.draw()
            fixation.draw()
            mywin.flip()
        
    run = True
    while run:
        Grt(direction)
        
        core.wait(0.1)
        keys = event.getKeys()
        if len(keys):        
            if keys[0] in ['q', 'escape']:
                run = False
                        
    mywin.close()