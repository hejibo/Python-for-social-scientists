# -*- coding: utf-8 -*-
#!/usr/bin/env python2

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from psychopy import visual,core, event

myWin = visual.Window((200.0,200.0))
myWin.setRecordFrameIntervals()

THoriLine = visual.Line(myWin,start=(0,0), end=(2.8,0))
THoriLine.draw()

TVertiLine = visual.Line(myWin,start=(0,0), end=(0,1.1))
TVertiLine.draw()
myWin.flip()

core.wait(5.0)


