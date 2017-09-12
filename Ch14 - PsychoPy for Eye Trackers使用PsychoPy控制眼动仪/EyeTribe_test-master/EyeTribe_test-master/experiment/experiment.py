# script to test eye trackers on four performance tests:
#	1) 9-point validation
#	2) natural scene viewing
#	3) pupil response to luminance change with central fixation
#	4) Saccades from left to right

# native
import os

# PyGaze
from constants import *
from pygaze.display import Display
from pygaze.screen import Screen
from pygaze.eyetracker import EyeTracker
from pygaze.keyboard import Keyboard
from pygaze.libtime import clock


# # # # #
# SETUP

# visuals
disp = Display()
scr = Screen()

# input
tracker = EyeTracker(disp)
kb = Keyboard(keylist=None, timeout=None)

# calibrate
tracker.calibrate()

# starting screen
scr.clear()
scr.draw_text(text="Press Space to start")
disp.fill(scr)
disp.show()
kb.get_key(keylist=['space'], timeout=None, flush=True)


# # # # #
# VALIDATION

# loop through points
for i in range(len(CALIBPOINTS)):
	# get coordinate
	x, y = CALIBPOINTS[i]
	# draw calibration point
	scr.clear()
	scr.draw_fixation(fixtype='dot', pos=(x,y))
	disp.fill(scr)
	# start recording
	tracker.start_recording()
	tracker.log("VALIDATION_TRIALSTART, trialnr=%d, x=%d, y=%d" % (i,x,y))
	# show display
	disp.show()
	tracker.log("validation_point_on")
	# allow for a bit of time so the subject can fixate the target
	clock.pause(1000)
	tracker.log("validation_point_fix")
	# wait for a bit
	clock.pause(POINTTIME)
	# clear screen
	scr.clear()
	disp.fill(scr)
	disp.show()
	# stop recording
	tracker.log("validation_point_off")
	tracker.stop_recording()
	# inter-trial interval
	clock.pause(ITI)

# pause screen
scr.clear()
scr.draw_text(text="Press Space to continue.")
disp.fill(scr)
disp.show()
kb.get_key(keylist=["space"], timeout=None, flush=True)


# # # # #
# IMAGES

# loop through images
for imgpath in IMAGES:
	# draw image
	scr.clear(colour=(255,255,255))
	scr.draw_image(imgpath)
	disp.fill(scr)
	# start recording
	tracker.start_recording()
	tracker.log("IMAGE_TRIALSTART")
	tracker.log("imgname=%s" % (os.path.basename(imgpath)))
	# show display
	disp.show()
	tracker.log("image_on")
	# wait for a bit
	clock.pause(IMGTIME)
	# clear screen
	scr.clear()
	disp.fill(scr)
	disp.show()
	# stop recording
	tracker.log("image_off")
	tracker.stop_recording()
	# inter-trial interval
	clock.pause(ITI)

# pause screen
scr.clear()
scr.draw_text(text="Press Space to continue.")
disp.fill(scr)
disp.show()
kb.get_key(keylist=["space"], timeout=None, flush=True)


# # # # #
# PUPIL TRIALS

# create screens
pupscr = {'black':Screen(),'white':Screen()}
pupscr['black'].clear(colour=(0,0,0))
pupscr['black'].draw_fixation(fixtype='dot', colour=(128,128,128))
pupscr['white'].clear(colour=(255,255,255))
pupscr['white'].draw_fixation(fixtype='dot', colour=(128,128,128))

# display first screen
curcol = 'white'
disp.fill(pupscr[curcol])
disp.show()
clock.pause(ITI)

# loop through all pupil trials
for i in range(PUPTRIALS):
	# reset colour
	if curcol == 'white':
		curcol = 'black'
	else:
		curcol = 'white'
	# draw new screen
	disp.fill(pupscr[curcol])
	# start recording
	tracker.start_recording()
	tracker.log("PUPIL_TRIALSTART, colour=%s" % (curcol))
	# baseline
	tracker.log("baseline_start")
	clock.pause(BASELINETIME)
	# display change
	disp.show()
	tracker.log("pupdata_start")
	clock.pause(PUPTRIALTIME)
	# stop recording
	tracker.log("pupdata_stop")
	tracker.stop_recording()
	# inter-trial interval
	clock.pause(ITI)

# pause screen
scr.clear()
scr.draw_text(text="Press Space to continue.")
disp.fill(scr)
disp.show()
kb.get_key(keylist=["space"], timeout=None, flush=True)


# # # # #
# SACCADE TRIALS

# create screens
sacscr = [Screen(), Screen()]
for i in range(len(sacscr)):
	sacscr[i].draw_fixation(fixtype='cross', pos=(int(DISPSIZE[0]*0.25),int(DISPSIZE[1]*0.5)))
sacscr[1].draw_fixation(fixtype='dot', pos=(int(DISPSIZE[0]*0.75),int(DISPSIZE[1]*0.5)))

# loop through all trials
for i in range(SACTRIALS):
	
	# ITI
	disp.fill()
	disp.show()
	clock.pause(ITI)
	
	# start tracking
	tracker.start_recording()
	tracker.log("SACC_TRIALSTART")
	
	# draw first screen
	disp.fill(sacscr[0])
	t0 = disp.show()
	tracker.log("fixation_on")
	
	# wait for a bit
	clock.pause(ITI)
	
	# wait until the cross is fixated
	fixated = False
	while not fixated:
		gazepos = tracker.sample()
		if ((gazepos[0]-int(DISPSIZE[0]*0.25))**2 + (gazepos[1]-int(DISPSIZE[1]*0.5))**2)**0.5 < 60:
			fixated = True
	
	# show target
	disp.fill(sacscr[1])
	t1 = disp.show()
	tracker.log("target_on")
	
	# wait until the target is fixated
	fixated = False
	while not fixated:
		gazepos = tracker.sample()
		if ((gazepos[0]-int(DISPSIZE[0]*0.75))**2 + (gazepos[1]-int(DISPSIZE[1]*0.5))**2)**0.5 < 60:
			fixated = True
	
	# wait for a bit more (to allow saccade to end)
	clock.pause(500)
	
	# stop tracking
	tracker.log("target_fixated")
	tracker.stop_recording()


# # # # #
# CLOSE

# show data transfer screen
scr.clear()
scr.draw_text(text="Transferring data, please wait...")
disp.fill(scr)
disp.show()

# neatly close connection to tracker
tracker.close()

# show ending screen
scr.clear()
scr.draw_text(text="Thanks for participating! Press Space to close.")
disp.fill(scr)
disp.show()
kb.get_key(keylist=["space"], timeout=None, flush=True)

# close display
disp.close()
