#!/usr/bin/env python2
from psychopy import core, visual, event
import psychopy.sound
#create a window to draw in
myWin = visual.Window((600,600))
myWin.setRecordFrameIntervals()
#INITIALISE SOME STIMULI
faceRGB = visual.ImageStim(myWin,image='face.jpg',
    pos=(0.0,0.0),
    size=(1.0,1.0))

faceRGB.draw()
myWin.flip()

#pause, so you get a chance to see it!
core.wait(5.0)

