'''
By DR. Jibo He @ uSEE Eye Tracking Inc. 
Written for my student at Chinese Academy of Science.
September 12, 2017
'''
#!/usr/bin/env python2
from psychopy import visual, core, event

#create a window to draw in
myWin = visual.Window((200.0,200.0),allowGUI=False,winType='pyglet',
            monitor='testMonitor', units ='deg', screen=0)
myWin.setRecordFrameIntervals()

#INITIALISE SOME STIMULI
square = visual.Rect(myWin,width=1,height=1)
square.pos= (0,0)
square.ori = 45
square.draw()
    

myWin.flip()
#pause, so you get a chance to see it!
core.wait(5.0)


