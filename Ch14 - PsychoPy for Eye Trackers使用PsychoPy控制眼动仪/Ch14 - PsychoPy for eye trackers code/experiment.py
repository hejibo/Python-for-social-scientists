# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 13:50:14 2017

@author: Dr.He
"""

import os
from constants import *
from pygaze.display import Display
from pygaze.screen import Screen
from pygaze.keyboard import Keyboard
from pygaze.eyetracker import EyeTracker
import pygaze.libtime as timer


# Initialise a Display to interact with the monitor
disp = Display()
# Initialise a Keyboard to collect key presses
kb = Keyboard(keylist=None, timeout=None)

# Create a Screen for the image task instructions
inscr = Screen()
inscr.draw_text(text='''Please look at the images. 
                \n\n(Press any key to begin)''', fontsize=24)

# Create a Screen with a central fixation cross
fixscr = Screen()
fixscr.draw_fixation(fixtype='cross', diameter=8)

# Create a Screen to draw images on later
imgscr = Screen()

# Initialise a new EyeTracker
tracker = EyeTracker(disp)
# Calibrate the eye tracker
tracker.calibrate()

# Feed the instructions to the Display
disp.fill(inscr)
# Show the instructions
disp.show()
# Wait until the participant presses any key
# (Allowing them to read the instructions at their own

   # pace)
kb.get_key()

# Choose the first image for now
imgname = IMGNAMES[0]
# Construct the path to the image
imgpath = os.path.join(IMGDIR, imgname)
# Draw the image on imgscr
# (clear imgscr first, to be sure it’s clean)
imgscr.clear()
imgscr.draw_image(imgpath)

# Start recording gaze data
tracker.start_recording()

# Display a status message on the EyeLink computer
# (EyeLink only; doesn’t do anything for other brands)
tracker.status_msg('Trial with %s image' % (imgname))
# Log trial start
tracker.log('TRIALSTART')

# Feed the fixation Screen to the Display
disp.fill(fixscr)
# Update the monitor to show the fixation mark
disp.show()
# Log the fixation onset to the gaze data file
tracker.log('fixation_onset')
# Wait for the right duration
timer.pause(FIXTIME)

# Feed the image Screen to the Display
disp.fill(imgscr)
# Update the monitor to show the image
disp.show()
# Log the image onset to the gaze data file
# Include the image name in the message!
tracker.log('image_onset, imgname=%s' % (imgname))
# Wait for the right duration
timer.pause(IMGTIME)

# Clear the Display
disp.fill()
# Update the monitor to show a blank screen
disp.show()
# Log the image offset
tracker.log('image_offset')

# Log the end of the trial
tracker.log('TRIALEND')
# Pause recording
tracker.stop_recording()

# Clear the instructions Screen
inscr.clear()

# Write a new message
inscr.draw_text(text='All done!', fontsize=24)
# Feed the new message to the Display
disp.fill(inscr)
# Show the message
disp.show()
# Wait until the participant presses any key
# (Allowing them to read at their own pace)
kb.get_key()

# Close the connection to the eye tracker
# (This will also close the log file!)
tracker.close()
# Close the Display
disp.close()
print "-_-!"