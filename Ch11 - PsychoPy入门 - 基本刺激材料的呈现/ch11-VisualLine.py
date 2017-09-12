#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from psychopy import visual, core, event

#create a window to draw in
myWin = visual.Window((200.0,200.0))
myWin.setRecordFrameIntervals()

#绘制水平线
THoriLine = visual.Line(myWin, start=(0, 0), end=(2.8, 0))
THoriLine.draw()

#绘制垂直线
TVertiLine = visual.Line(myWin, start=(0, 0), end=(0, 1.1))
TVertiLine.draw()
    
myWin.flip()

#pause, so you get a chance to see it!
core.wait(5.0)


