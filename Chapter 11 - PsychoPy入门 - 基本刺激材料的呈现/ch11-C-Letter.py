#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from psychopy import visual, core, event

#create a window to draw in
myWin = visual.Window((800.0,800.0),allowGUI=False,winType='pyglet',
            monitor='testMonitor', units ='deg', screen=0)
myWin.setRecordFrameIntervals()


#INITIALISE SOME STIMULI
circle = visual.Circle(myWin, radius=2, edges=32)
circle.pos=(0,0)
circle.draw()

THoriLine = visual.Line(myWin,start=(1.9,0), end=(2.1,0))
THoriLine.lineColor = 'grey'
THoriLine.lineWidth = 30


THoriLine.draw()

myWin.flip()
#pause, so you get a chance to see it!
core.wait(5.0)


