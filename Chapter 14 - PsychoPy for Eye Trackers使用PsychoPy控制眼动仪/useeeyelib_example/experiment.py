#pip install pygame

# native
import os

# external
import pygame

# custom
from useeeyelib import uSeeEyeLib


# # # # #
# CONSTANTS

# screen stuff
RESOLUTION = (1600,900)
BGC = (0,0,0)

# files and paths
DIR = os.path.dirname(os.path.abspath(__file__))
LOGFILE = os.path.join(DIR, 'example_data.txt')
IMGDIR = os.path.join(DIR, 'imgs')
IMGNAMES = os.listdir(IMGDIR)


# # # # #
# PREPARE

# start communications with the uSEE tracker
tracker = uSeeEyeLib(logfilename=LOGFILE)

# initialize PyGame
pygame.init()

# create a new display
disp = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)

# compile a list of images
images = {}
for filename in IMGNAMES:
	# check if the extension is a JPEG image
	if os.path.splitext(filename)[1] == '.jpg':
		# load the image, and add to the image dict
		images[filename] =  pygame.image.load(os.path.join(IMGDIR,filename))


# # # # #
# RUN

# loop through all images
for imgname in images.keys():
	print imgname
	# blit the image
	blitpos = (RESOLUTION[0]/2 - images[imgname].get_width()/2,
			RESOLUTION[1]/2 - images[imgname].get_height()/2)
	disp.blit(images[imgname], blitpos)

	# start recording gaze data
	tracker.start_recording()
	
	# show the image
	pygame.display.flip()
	tracker.log_message("image_on")
	tracker.log_message(imgname)
	
	# wait for a bit
	pygame.time.wait(5000)
	
	# show a blank screen
	disp.fill(BGC)
	pygame.display.flip()
	tracker.log_message("image_off")
	
	# stop recording
	tracker.stop_recording()

	# wait for a bit
	pygame.time.wait(2000)


# # # # #
# CLOSE

# close connection to the tracker
tracker.close()

# close the display
pygame.quit()
