#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from psychopy import visual, core, event

myWin = visual.Window((800.0,800.0),
            monitor='testMonitor', units ='deg', screen=0)
myWin.setRecordFrameIntervals()

red = visual.TextStim(myWin, color='red',
                        text = u"red",
                        units='norm', height=0.1,
                        pos=[0, -0.1], alignHoriz='right',alignVert='top')
                        
green = visual.TextStim(myWin, color='green',
                        text = u"green",
                        units='norm', height=0.1,
                        pos=[0, 0], alignHoriz='right',alignVert='top')
                        
blue = visual.TextStim(myWin, color='blue',
                        text = u"black",
                        units='norm', height=0.1,
                        pos=[0, 0.1], alignHoriz='right',alignVert='top')                       

red.draw()
green.draw()
blue.draw()
    
myWin.flip()

core.wait(15.0)