import os

# main
DIR = os.path.abspath(os.path.dirname(__file__))
IMGDIR = os.path.join(DIR, 'imgs')
DATADIR = os.path.join(DIR, 'data')
#LOGFILENAME = raw_input("Participant: ")
#LOGFILE = os.path.join(DATADIR, LOGFILENAME)

# display
DISPTYPE = 'pygame'
DISPSIZE = (1024,768)

# validation points
PXY = [0.15, 0.5, 0.85]
CALIBPOINTS = []
for x in PXY:
	for y in PXY:
		CALIBPOINTS.append((int(x*DISPSIZE[0]),(int(y*DISPSIZE[1]))))

# images
IMAGES = []
for imgname in os.listdir(IMGDIR):
	IMAGES.append(os.path.join(IMGDIR, imgname))

# light-dark
PUPTRIALS = 50
SACTRIALS = 50

# timing
ITI = 1000
POINTTIME = 2000
IMGTIME = 10000
BASELINETIME = 200
PUPTRIALTIME = 2500

# trackers
TRACKERTYPE = 'eyetribe'
DUMMYMODE = False
