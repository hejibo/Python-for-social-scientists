# script to analyse all participants' data on an eye tracker performance
# tests, including the following elements:
#	1) 9-point validation
#	2) natural scene viewing
#	3) pupil response to luminance change with central fixation
#	4) Saccades from left to right

# native
import os
import pickle

# constants from experiment
from constants import *

# custom
import pyenalysis
from pygazeanalyser import gazeplotter

# external
import numpy
from matplotlib import pyplot


# # # # #
# CONSTANTS

# list of analyses that are to be run
OPTIONS = ['validation', 'images', 'pupilometry', 'saccadometry', 'samplerate']

# excluded participants
EXCL = ['ED_pupil']

# settings
TRACKERS = ['eyelink', 'eyetribe']

# paths and files
DIR = os.path.dirname(os.path.abspath(__file__))
IMGDIR = os.path.join(DIR, 'imgs')
DATADIR = os.path.join(DIR, 'data')
IOUTDIR = os.path.join(DIR, 'output')
OUTDIR = os.path.join(IOUTDIR, 'group_data')

# plotting
# (Tango colours: http://tango.freedesktop.org/Tango_Icon_Theme_Guidelines)
DPI = 100.0
FIGSIZE = (DISPSIZE[0]/DPI, DISPSIZE[1]/DPI)
PLOTCOLS = {	'raw':		'#2e3436',
			'validation':	'#4e9a06',
			'white':		'#c4a000',
			'black':		'#204a87',
			'eyelink':		'#204a87',
			'eyetribe':		'#a40000',
			'significant':	'#babdb6',
			'pupscreenonset':'#4e9a06'
			}

# checks
if not os.path.isdir(DATADIR):
	raise Exception("ERROR: no data directory found! (expecting '%s')" % DATADIR)
if 'images' in OPTIONS and not os.path.isdir(IMGDIR):
	raise Exception("ERROR: no image directory found! (expecting '%s')" % IMGDIR)
if not os.path.isdir(IOUTDIR):
	os.mkdir(IOUTDIR)
if not os.path.isdir(OUTDIR):
	os.mkdir(OUTDIR)


# # # # #
# INDIVIDUAL ANALYSES

# autodetect all participants
PPS = []
for filename in os.listdir(DATADIR):
	if os.path.isfile(os.path.join(DATADIR, filename)):
		name, ext = os.path.splitext(filename)
		if ext in ['.asc', '.tsv']:
			if name not in PPS:
				PPS.append(name)
print("Found %d participants." % (len(PPS)))

# exclude participants
for ppname in EXCL:
	excluded = PPS.pop(PPS.index(ppname))
	print("Excluded '%s'" % excluded)

# run all individual analyses
for ppname in PPS:
	# assemble a list of all command options
	cmdlist = ["python", "analysis_v2.py", ppname]
	cmdlist.extend(OPTIONS)
	# make an actual command out of the string
	cmd = ' '.join(cmdlist)
	# run the command
	print("Now running '%s'" % cmd)
	returncode = os.system(cmd)
	print("Done! Return code %d" % returncode)
	# check if it went ok
	ok = returncode == 0
	# raise Exception if there was a problem
	if not ok:
		raise Exception("ERROR: the following command did not return ok '%s'" % cmd)


# # # # #
# GROUP ANALYSES

# VALIDATION
if 'validation' in OPTIONS:
	
	# ALL SAMPLES PLOT
	print("Plotting all validation samples.")
	# open new figure
	fig, ax = pyplot.subplots(nrows=1, ncols=1)
	fig.set_dpi(DPI)
	fig.set_size_inches(FIGSIZE, forward=True)
	# loop through all participants
	for ppname in PPS:
		# loop through all tracker types
		for trackertype in TRACKERS:
			# load their data
			x = numpy.load(os.path.join(IOUTDIR, ppname, trackertype, 'validation_x.npy'))
			y = numpy.load(os.path.join(IOUTDIR, ppname, trackertype, 'validation_y.npy'))
			# plot all samples
			ax.plot(x, y, 'o', markersize=1, markeredgewidth=0, c=PLOTCOLS[trackertype])
	# loop through calibration points
	for i in range(len(CALIBPOINTS)):
		# plot validation points
		ax.plot(CALIBPOINTS[i][0], CALIBPOINTS[i][1], 'o', markersize=6, c=PLOTCOLS['validation'], alpha=0.5)
	# finish figure
	ax.axis([0, DISPSIZE[0], 0, DISPSIZE[1]])
	ax.invert_yaxis()
	#oax.legend()
	ax.set_xlabel("display x coordinate (pixels)")
	ax.set_ylabel("display y coordinate (pixels)")
	# save plot
	fig.savefig(os.path.join(OUTDIR, "validation_all_samples.png"))
	# close figure
	pyplot.close(fig)
	
	# PRECISION AND ACCURACY AVERAGES
	# empty dicts
	precision = {'x':[], 'y':[]}
	accuracy = {'x':[], 'y':[]}
	# collect all data
	for trackertype in TRACKERS:
		for ppname in PPS:
			# read data file
			datafile = open(os.path.join(IOUTDIR, ppname, trackertype, "accuracy_and_precision.txt"), 'r')
			data = datafile.readlines()
			datafile.close()
			# parse data
			for i in range(len(data)):
				data[i] = data[i].replace('\n','').replace('\r','').replace('"','').replace("'","").split('\t')
			header = data.pop(0)
			# add data to list
			precision['x'].append(float(data[0][header.index('precision_x')]))
			precision['y'].append(float(data[0][header.index('precision_y')]))
			accuracy['x'].append(float(data[0][header.index('accuracy_x')]))
			accuracy['y'].append(float(data[0][header.index('accuracy_y')]))
		# write data to file
		txtf = open(os.path.join(OUTDIR, "averages_%s_accuracy_and_precision.txt" % trackertype), 'w')
		txtf.write('\t'.join(['precision_x', 'precision_y', 'accuracy_x', 'accuracy_y']) + '\n')
		txtf.write('\t'.join(map(str, [numpy.mean(precision['x']), numpy.mean(precision['y']), numpy.mean(accuracy['x']), numpy.mean(accuracy['y'])])))
		txtf.close()



# # # # #
# IMAGES

# FIXATION VISUALISATION
if 'images' in OPTIONS:
	# loop through all trackers
	for trackertype in TRACKERS:
		# loop through all images
		for imgname in IMAGES:
			# get rid of image path and extension
			imgname, ext = os.path.splitext(os.path.basename(imgname))
			# empty lists
			fixations = []
			# loop through all participants
			for ppname in PPS:
				fixfile = open(os.path.join(IOUTDIR, ppname, trackertype, "fixations_%s.dat" % imgname), 'r')
				fixations.extend(pickle.load(fixfile))
				fixfile.close()
			# plot fixations
			fig = gazeplotter.draw_fixations(fixations, DISPSIZE, imagefile=os.path.join(IMGDIR, "%s%s" % (imgname,ext)), durationsize=True, durationcolour=False, alpha=0.5, savefilename=os.path.join(OUTDIR, "fixations_%s_%s.png" % (trackertype,imgname)))
			pyplot.close(fig)
			# create heatplot
			fig = gazeplotter.draw_heatmap(fixations, DISPSIZE, imagefile=os.path.join(IMGDIR, "%s%s" % (imgname,ext)), durationweight=True, alpha=0.5, savefilename=os.path.join(OUTDIR, "heatmap_%s_%s.png" % (trackertype,imgname)))
			pyplot.close(fig)
	
		# PRECISION AND ACCURACY AVERAGES
		# empty dicts
		alldata = {}
		for ppname in PPS:
			# read data file
			datafile = open(os.path.join(IOUTDIR, ppname, trackertype, "ROI_analysis.txt"), 'r')
			data = datafile.readlines()
			datafile.close()
			# parse data
			for i in range(len(data)):
				data[i] = data[i].replace('\n','').replace('\r','').replace('"','').replace("'","").split('\t')
			header = data.pop(0)
			# loop through all fields in the header
			for roi in header:
				# only proceed if the header field is an ROI
				if roi != '':
					# add a new entry to the dict for this ROI
					if not roi in alldata.keys():
						alldata[roi] = {}
					# loop through all lines of data
					# (consisting of three measure per AOI: Nfix,
					# fixdur, and dwelltime)
					for i in range(len(data)):
						# get the measure
						m = data[i][0]
						# add a new entry to the dict
						if m not in alldata[roi].keys():
							alldata[roi][m] = []
						# add data to the dict
						alldata[roi][m].append(float(data[i][header.index(roi)]))
		# write data to file
		rois = alldata.keys()
		header = ['']
		header.extend(rois)
		txtf = open(os.path.join(OUTDIR, "averages_%s_ROI_analysis.txt" % trackertype), 'w')
		txtf.write('\t'.join(header) + '\n')
		for m in alldata[rois[0]].keys():
			outline = [m]
			for roi in rois:
				outline.append(numpy.mean(alldata[roi][m]))
			txtf.write('\t'.join(map(str, outline)) + '\n')
		txtf.close()


# # # # #
# SACCADES

if 'saccadometry' in OPTIONS:
	
	for trackertype in TRACKERS:

		# INDIVIDUAL DATA
		# empty dicts
		alldata = {}
		for ppname in PPS:
			# read data file
			datafile = open(os.path.join(IOUTDIR, ppname, trackertype, "saccadometry_indices.txt"), 'r')
			data = datafile.readlines()
			datafile.close()
			# parse data
			for i in range(len(data)):
				data[i] = data[i].replace('\n','').replace('\r','').replace('"','').replace("'","").split('\t')
			header = data.pop(0)
			# loop through all fields in the header
			for m in header:
				# only proceed if the header field is an actual index
				if m != '':
					# add a new entry to the dict for this index
					if not m in alldata.keys():
						alldata[m] = {}
					# get the first line of data
					# (containing the averages)
					# add a new entry to the dict
					if not 'M' in alldata[m].keys():
						alldata[m]['M'] = []
					# add data to the dict
					alldata[m]['M'].append(float(data[0][header.index(m)]))
	
		# GROUP DATA
		# write header to new file
		ms = alldata.keys()
		header = ['']
		header.extend(ms)
		txtf = open(os.path.join(OUTDIR, "averages_%s_saccadometry.txt" % trackertype), 'w')
		txtf.write('\t'.join(header) + '\n')
		# write line with group averages
		outline = ['M']
		for m in ms:
			outline.append(numpy.mean(alldata[m]['M']))
		txtf.write('\t'.join(map(str, outline)) + '\n')
		# write line with group standard deviations
		outline = ['SD']
		for m in ms:
			outline.append(numpy.std(alldata[m]['M']))
		txtf.write('\t'.join(map(str, outline)) + '\n')
		# close file
		txtf.close()


# # # # #
# SAMPLING

if 'samplerate' in OPTIONS:
	
	for trackertype in TRACKERS:

		# INDIVIDUAL DATA
		# empty dicts
		alldata = {}
		for ppname in PPS:
			# read data file
			datafile = open(os.path.join(IOUTDIR, ppname, trackertype, "intersample_times.txt"), 'r')
			data = datafile.readlines()
			datafile.close()
			# parse data
			for i in range(len(data)):
				data[i] = data[i].replace('\n','').replace('\r','').replace('"','').replace("'","").split('\t')
			header = data.pop(0)
			# loop through all fields in the header
			for m in header:
				# only proceed if the header field is an actual index
				if m != 'intersample time':
					# add a new entry to the dict for this index
					if not m in alldata.keys():
						alldata[m] = []
					# add data to the dict
					alldata[m].append(float(data[0][header.index(m)]))
	
		# GROUP DATA
		# write header to new file
		ms = alldata.keys()
		ms.sort()
		header = ['']
		header.extend(ms)
		txtf = open(os.path.join(OUTDIR, "averages_%s_sampling.txt" % trackertype), 'w')
		txtf.write('\t'.join(header) + '\n')
		# write line with group sum
		outline = ['M']
		for m in ms:
			outline.append(numpy.sum(alldata[m]))
		txtf.write('\t'.join(map(str, outline)) + '\n')
		# close file
		txtf.close()
