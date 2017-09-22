# This is an script example of how to use the pytribe.EyeTribe class to track
# gaze data while a participant is looking at some images. Please note that
# the experiment assumes that you have calibrated the eye tracker beforehand,
# using the EyeTribe UI.
#
# Data analysis will be performed directly after running the experiment, using
# PyGazeAnalyser (see: https://github.com/esdalmaijer/PyGazeAnalyser)
#
# The folder in which this script is placed, should contain the following:
#	- example.py (script to show images)
#	- analysis.py (this script)
#	- pytribe.py (script to communicate with the EyeTribe tracker,
#		from: https://github.com/esdalmaijer/PyTribe/blob/master/pytribe.py)
#	- imgs (folder containing images,
#		from: https://github.com/esdalmaijer/PyGazeAnalyser/tree/master/examples/analysis/imgs)
#	- pygazeanalyser (folder containing analysis routines for gaze data,
#		from: https://github.com/esdalmaijer/PyGazeAnalyser/tree/master/pygazeanalyser)
#
# author: Edwin Dalmaijer
# email: edwin.dalmaijer@psy.ox.ac.uk
#
# version 1 (02-Jul-2014)

# native
import os

# custom
from pygazeanalyser import eyetribereader, gazeplotter


# # # # #
# CONSTANTS

# screen stuff
RESOLUTION = (1280,1024)
BGC = (0,0,0)

# files and paths
DIR = os.path.dirname(os.path.abspath(__file__))
LOGFILE = os.path.join(DIR, 'example_data.txt')
IMGDIR = os.path.join(DIR, 'imgs')
IMGNAMES = os.listdir(IMGDIR)


# # # # #
# ANALYSIS

# create a new output directory
outdir = os.path.join(DIR, 'output')
if not os.path.isdir(outdir):
	os.mkdir(outdir)

# read the data file
gazedata = eyetribereader.read_eyetribe(LOGFILE, "image_on", stop="image_off", missing=0.0)

# loop through all trials
for trialnr in range(len(gazedata)):
	
	# find the image file name
	for msg in gazedata[trialnr]['events']['msg']:
		if '.jpg' in msg[1]:
			imgname = os.path.splitext(msg[1])[0]
			imgfile = os.path.join(IMGDIR,msg[1])
	
	# get the fixations
	fixations = gazedata[trialnr]['events']['Efix']
	
	# plot the samples
	gazeplotter.draw_raw(gazedata[trialnr]['x'],gazedata[trialnr]['y'], RESOLUTION,
					imagefile=imgfile, savefilename=os.path.join(outdir,'%s_samples.png' % imgname))
	# plot the fixations
	gazeplotter.draw_fixations(fixations, RESOLUTION, imagefile=imgfile, durationsize=True,
					durationcolour=False, alpha=0.5, savefilename=os.path.join(outdir,'%s_fixations.png' % imgname))
	# plot a heatmap
	gazeplotter.draw_heatmap(fixations, RESOLUTION, imagefile=imgfile, durationweight=True,
					alpha=0.5, savefilename=os.path.join(outdir,'%s_heatmap.png' % imgname))
	 
