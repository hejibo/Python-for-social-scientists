#pip install matplotlib
#pip install pillow

# native
import os

# custom
from pygazeanalyser import eyetribereader, gazeplotter

# # # # #
# CONSTANTS

# screen stuff
RESOLUTION = (1600,900)
BGC = (0,0,0)

# files and paths
DIR = os.path.dirname(os.path.abspath(__file__))
LOGFILE = os.path.join(DIR, 'example_data.txt.tsv')
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
	 
