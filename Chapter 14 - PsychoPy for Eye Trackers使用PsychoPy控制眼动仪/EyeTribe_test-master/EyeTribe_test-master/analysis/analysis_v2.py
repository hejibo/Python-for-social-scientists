# script to analyse a single participant's data on an eye tracker performance
# tests, including the following elements:
#	1) 9-point validation
#	2) natural scene viewing
#	3) pupil response to luminance change with central fixation
#	4) Saccades from left to right

# native
import os
import sys
import copy
import pickle

# constants from experiment
from constants import *

# custom
import pyenalysis
from pygazeanalyser import gazeplotter
from pygazeanalyser.eyetribereader import read_eyetribe
from pygazeanalyser.edfreader import read_edf
from pygazeanalyser.detectors import fixation_detection
from ROIs.ROIs_28m_HA_O import ROIS, ROILIST

# external
import numpy
from numpy import nanmean, nanstd
from scipy.stats import ttest_rel
from matplotlib import pyplot


# # # # #
# COMMAND LINE ARGUMENTS

# default settings
DOVALIDATION = False
DOIMAGES = False
DOPUPILOMETRY = False
DOSACCADES = False
DOINTSAMPLETIME = False

print("\tRunning the analysis with the following options:")
if len(sys.argv) == 1:
	# default participant name
	PPNAME = "ED"
	print("\t\tparticipant '%s'" % PPNAME)
else:
	# participant name
	PPNAME = sys.argv[1]
	print("\t\tparticipant '%s'" % PPNAME)
	# update settings
	if 'validation' in sys.argv:
		print("\t\tvalidation")
		DOVALIDATION = True
	if 'images' in sys.argv:
		print("\t\timages")
		DOIMAGES = True
	if 'pupilometry' in sys.argv:
		print("\t\tpupilometry")
		DOPUPILOMETRY = True
	if 'saccadometry' in sys.argv:
		print("\t\tsaccadometry")
		DOSACCADES = True
	if 'samplerate' in sys.argv:
		print("\t\tsamplerate")
		DOINTSAMPLETIME = True


# # # # #
# CONSTANTS

# fixation detection
FIXTHRESH = 1 # degree of visual angle
FIXMINDUR = 50 # milliseconds

# pupilometry
PUPALPHA = 0.000025
PUPAXES = [0, 2000, 0.5, 1.6]
EYELINKPUPTYPE = 'DIAMETER'

# saccade detection
MAXDISP = 0.25 # degrees of visual angle; maximal horizontal dispersion from fixation
MAXENDERR = 0.75 # degrees of visual angle; maximal distance from target
MINSACDUR = 20 # milliseconds
FIXPOS = (DISPSIZE[0] * 0.25, DISPSIZE[1] * 0.5)
TARPOS = (DISPSIZE[0] * 0.75, DISPSIZE[1] * 0.5)
VELTHRESH = 20 # degrees per second
ACCTHRESH = 9500 # degrees per second**2
SCREENDIST = 62.0 # cm
SCREENSIZE = (40.5,30.5) # cm
PIXPERCM = numpy.mean([DISPSIZE[0]/SCREENSIZE[0], DISPSIZE[1]/SCREENSIZE[1]])

# files
OUTSEP = '\t'
OUTDIR = os.path.join(DIR, 'output', PPNAME)

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
if DOIMAGES and not os.path.isdir(IMGDIR):
	raise Exception("ERROR: no image directory found! (expecting '%s')" % IMGDIR)
if not os.path.isdir(OUTDIR):
	os.mkdir(OUTDIR)


# # # # #
# CUSTOM FUNCTIONS

def cm2ang(stimsize, stimdist):
	
	"""
	desc:
		Calculates the size of a stimulus (or any other kind of distance on
		the display) in degrees of visual angle, based on the size of the
		stimulus in centimeters, and the distance between the stimulus and
		the observer in centimeters.
	
	arguments:
		stimsize:
			desc:	Stimulus (or other on-screen distance) size in cm.
			type:	[int, float, numpy.array]
		stimdist:
			desc:	Distance between display and observer in cm.
			type:	[float, int]
	
	returns:
		The stimulus size in degrees of visual angle.
	
	"""
	
	return numpy.rad2deg(2 * numpy.arctan(stimsize / (2*stimdist)))

def ang2cm(stimsize, stimdist):
	
	"""
	desc:
		Calculates the size of a stimulus (or any other kind of distance on
		the display) in centimeters, based on the size of the stimulus in
		degrees of visual angle, and the distance between the stimulus and
		the observer in centimeters.
	
	arguments:
		stimsize:
			desc:	Stimulus (or other on-screen distance) size in degrees.
			type:	[int, float, numpy.array]
		stimdist:
			desc:	Distance between display and observer in cm.
			type:	[float, int]
	
	returns:
		The stimulus size in centimeters.
	
	"""
	
	return 2*stimdist * numpy.tan(numpy.deg2rad(stimsize)/2)


# # # # #
# DATA TYPE

# data reading functions
read_data = {'eyelink':read_edf, 'eyetribe':read_eyetribe}

# overall plot for validation
if DOVALIDATION:
	# open new figure
	sofig, soax = pyplot.subplots(nrows=1, ncols=1)
	sofig.set_dpi(DPI)
	sofig.set_size_inches(FIGSIZE, forward=True)

# loop through both trackers' data
for trackertype in ['eyelink', 'eyetribe']:
	
	# TRACKER SPECIFIC SETTINGS
	# check if there is an output directory; if not, create one
	outputdir = os.path.join(OUTDIR, trackertype)
	if not os.path.isdir(outputdir):
		os.mkdir(outputdir)
	# get the correct text file
	if trackertype == 'eyelink':
		DATAFILE = os.path.join(DATADIR, '%s.asc' % PPNAME)
	elif trackertype == 'eyetribe':
		DATAFILE = os.path.join(DATADIR, '%s.tsv' % PPNAME)
	# amount of samples in pupilometry data
	if trackertype == 'eyelink':
		# 2 seconds, sampling rate 1000 Hz
		pupilsamples = 2000
		baselinpupilsamples = 199
		samplingrate = 1000
	elif trackertype == 'eyetribe':
		# 2 seconds, sampling rate 60 Hz
		pupilsamples = 120
		baselinpupilsamples = 9
		samplingrate = 60
	
	
	# # # # #
	# VALIDATION
	
	if DOVALIDATION:
		
		# empty list to collect random and systematic error
		randl = {'x':[], 'y':[]}
		sysl = {'x':[], 'y':[]}
	
		# READ DATA
		validationdata = read_data[trackertype](DATAFILE, "validation_point_fix", stop="validation_point_off", missing=0.0, debug=False)

		# STORE AND PLOT DATA
		# arrays to save in NumPy file
		allx = numpy.array([])
		ally = numpy.array([])
		# overall plot
		# open new figure
		ofig, oax = pyplot.subplots(nrows=1, ncols=1)
		ofig.set_dpi(DPI)
		ofig.set_size_inches(FIGSIZE, forward=True)
		# individual plots
		for i in range(len(validationdata)):

			# add to error lists
			randl['x'].extend(list(numpy.diff(validationdata[i]['x'][validationdata[i]['x']>0])))
			randl['y'].extend(list(numpy.diff(validationdata[i]['y'][validationdata[i]['y']>0])))
			sysl['x'].extend(list(validationdata[i]['x'][validationdata[i]['x']>0] - CALIBPOINTS[i][0]))
			sysl['y'].extend(list(validationdata[i]['y'][validationdata[i]['y']>0] - CALIBPOINTS[i][1]))

			# add arrays to lists
			allx = numpy.hstack((allx, validationdata[i]['x']))
			ally = numpy.hstack((ally, validationdata[i]['y']))

			# open new figure
			fig, ax = pyplot.subplots(nrows=1, ncols=1)
			fig.set_dpi(DPI)
			fig.set_size_inches(FIGSIZE, forward=True)
			# plot all samples
			ax.plot(validationdata[i]['x'], validationdata[i]['y'], 'o', c=PLOTCOLS['raw'], label='samples')
			oax.plot(validationdata[i]['x'], validationdata[i]['y'], 'o', c=PLOTCOLS['raw'])
			soax.plot(validationdata[i]['x'], validationdata[i]['y'], 'o', markersize=1, markeredgewidth=0, c=PLOTCOLS[trackertype])
			# plot validation point
			ax.plot(CALIBPOINTS[i][0], CALIBPOINTS[i][1], 'o', markersize=12, c=PLOTCOLS['validation'], label='stimulus')
			oax.plot(CALIBPOINTS[i][0], CALIBPOINTS[i][1], 'o', markersize=12, c=PLOTCOLS['validation'])
			soax.plot(CALIBPOINTS[i][0], CALIBPOINTS[i][1], 'o', markersize=6, c=PLOTCOLS['validation'], alpha=0.5)
			# finish plot
			ax.axis([0, DISPSIZE[0], 0, DISPSIZE[1]])
			ax.invert_yaxis()
			ax.legend()
			# save plot
			fig.savefig(os.path.join(outputdir, "validationpoint_%d_%d.png" % (CALIBPOINTS[i][0], CALIBPOINTS[i][1])))
			# close figure
			pyplot.close(fig)

		# save files with x and y coordinates
		numpy.save(os.path.join(outputdir, 'validation_x.npy'), allx)
		numpy.save(os.path.join(outputdir, 'validation_y.npy'), ally)

		# finish overall figure
		oax.axis([0, DISPSIZE[0], 0, DISPSIZE[1]])
		oax.invert_yaxis()
		#oax.legend()
		# save plot
		ofig.savefig(os.path.join(outputdir, "validationpoint_all.png"))
		# close figure
		pyplot.close(ofig)
		
		# ACCURACY AND PRECISION
		# calculate values
		RMS = {}
		acc = {}
		for d in ['x', 'y']:
			RMS[d] = cm2ang(((numpy.mean(numpy.array(randl[d]))**2)**0.5)/PIXPERCM, SCREENDIST)
			acc[d] = cm2ang(numpy.mean(numpy.array(sysl[d]))/PIXPERCM, SCREENDIST)
		# write a report to a new text file
		txtf = open(os.path.join(outputdir, "accuracy_and_precision.txt"), 'w')
		txtf.write(OUTSEP.join(['precision_x', 'precision_y', 'accuracy_x', 'accuracy_y']) + '\n')
		txtf.write(OUTSEP.join(map(str, [RMS['x'], RMS['y'], acc['x'], acc['y']])))
		txtf.close()


	# # # # #
	# IMAGES
	
	if DOIMAGES:

		# READ DATA
		imagedata = read_data[trackertype](DATAFILE, "image_on", stop="image_off", missing=0.0, debug=False)
		
		# CUSTOM FIXATION DETECTION
		# calculate maximal inter-sampel distance
		maxdist = ang2cm(FIXTHRESH, SCREENDIST) * PIXPERCM
		# overwrite fixations
		for i in range(len(imagedata)):
			imagedata[i]['events']['Sfix'], imagedata[i]['events']['Efix'] = \
				fixation_detection(imagedata[i]['x'], imagedata[i]['y'], imagedata[i]['trackertime'], missing=0.0, maxdist=maxdist, mindur=FIXMINDUR)

		# PLOT DATA
		for i in range(len(imagedata)):
			# image name
			imgname = os.path.splitext(os.path.basename(IMAGES[i]))[0]
			# pickle fixation data
			fixfile = open(os.path.join(outputdir, "fixations_%s.dat" % imgname), 'w')
			pickle.dump(imagedata[i]['events']['Efix'], fixfile)
			fixfile.close()
			# plot raw data
			fig = gazeplotter.draw_raw(imagedata[i]['x'], imagedata[i]['y'], DISPSIZE, imagefile=IMAGES[i], savefilename=os.path.join(outputdir, "image_%s_raw.png" % imgname))
			pyplot.close(fig)
			# plot fixations
			fig = gazeplotter.draw_fixations(imagedata[i]['events']['Efix'], DISPSIZE, imagefile=IMAGES[i], durationsize=True, durationcolour=False, alpha=0.5, savefilename=os.path.join(outputdir, "image_%s_fixations.png" % imgname))
			pyplot.close(fig)
			# draw heatmap
			fig = gazeplotter.draw_heatmap(imagedata[i]['events']['Efix'], DISPSIZE, imagefile=IMAGES[i], durationweight=True, alpha=0.5, savefilename=os.path.join(outputdir, "image_%s_heatmap.png" % imgname))
			pyplot.close(fig)
		
			# ROI ANALYSIS
			if "01F_HA_O" in IMAGES[i]:
				# empty dicts
				Nfix = {}
				fixdur = {}
				dwelltime = {}
				# go through all ROI names
				for ROIname in ROILIST:
					# starting values
					Nfix[ROIname] = 0
					fixdur[ROIname] = 0
					dwelltime[ROIname] = 0
				# go through all fixations
				for stime, etime, dur, sx, sy in imagedata[i]['events']['Efix']:
					for ROIname in ROILIST:
						if ROIS[ROIname][0] <= sx <= ROIS[ROIname][0]+ROIS[ROIname][2] \
							and ROIS[ROIname][1] <= sy <= ROIS[ROIname][1]+ROIS[ROIname][3]:
								Nfix[ROIname] += 1
								dwelltime[ROIname] += dur
								break
				# calculate average fixation time
				for ROIname in ROILIST:
					if Nfix[ROIname] > 0:
						fixdur[ROIname] = dwelltime[ROIname] / Nfix[ROIname]
				# write data to textfile
				txtfile = open(os.path.join(outputdir, "ROI_analysis.txt"), 'w')
				txtfile.write('\t' + OUTSEP.join(ROILIST) + '\n')
				content = [['Nfix'],['fixdur'],['dwelltime']]
				for ROIname in ROILIST:
					content[0].append(Nfix[ROIname])
					content[1].append(fixdur[ROIname])
					content[2].append(dwelltime[ROIname])
				txtfile.write(OUTSEP.join(map(str, content[0])) + '\n')
				txtfile.write(OUTSEP.join(map(str, content[1])) + '\n')
				txtfile.write(OUTSEP.join(map(str, content[2])))
				txtfile.close()
	
	
	# # # # #
	# PUPILOMETRY
	
	if DOPUPILOMETRY:
		
		# correct STUPID mistake (forgot to set pupil measure to DIAMETER)
		DATAFILE = DATAFILE.replace('ED.asc', 'ED_pupil.asc')
	
		# READ DATA
		pupildata = read_data[trackertype](DATAFILE, "PUPIL_TRIALSTART", stop="pupdata_stop", missing=0.0, debug=False)
		baseline = {'white':[], 'black':[]}
		pupresponse = {'white':[], 'black':[]}
		traces = {'white':[], 'black':[]}
		
		# PARSE DATA
		for i in range(len(pupildata)):
			# conditions
			t0, msg = pupildata[i]['events']['msg'][0]
			if 'white' in msg:
				condition = 'white'
			else:
				condition = 'black'
			# baseline (t1) and stimonset (t2)
			t1, msg = pupildata[i]['events']['msg'][1]
			t2, msg = pupildata[i]['events']['msg'][2]
			# add pupildata to baseline
			bsi = numpy.argmin(numpy.abs(pupildata[i]['trackertime']-t1))
			bei = numpy.argmin(numpy.abs(pupildata[i]['trackertime']-t2))
			while bei - bsi > baselinpupilsamples:
				bsi += 1
			baseline[condition].append(pupildata[i]['size'][bsi:bei])
			pupresponse[condition].append(pupildata[i]['size'][bei:bei+pupilsamples])
			puptime = pupildata[i]['time'][bei:bei+pupilsamples]
			basepuptime = pupildata[i]['time'][bsi:bei]
		
		# CLEAN UP DATA
		for condition in baseline.keys():
			for i in range(len(baseline[condition])):
				# recalculate EyeLink AREA to DIAMETER
				if trackertype == 'eyelink' and EYELINKPUPTYPE == 'AREA':
					baseline[condition][i] = ((baseline[condition][i] / numpy.pi)**0.5) * 2
					pupresponse[condition][i] = ((pupresponse[condition][i] / numpy.pi)**0.5)*2
				# interpolate missing
				baseline[condition][i] = pyenalysis.interpolate_missing(baseline[condition][i], mindur=1, invalid=0.0)
				pupresponse[condition][i] = pyenalysis.interpolate_missing(pupresponse[condition][i], mindur=1, invalid=0.0)
				# interpolate blinks
				baseline[condition][i] = pyenalysis.interpolate_blink(baseline[condition][i], mode='auto', invalid=0.0, edfonly=False)
				pupresponse[condition][i] = pyenalysis.interpolate_blink(pupresponse[condition][i], mode='auto', invalid=0.0, edfonly=False)
				# hampel
				baseline[condition][i] = pyenalysis.hampel(baseline[condition][i])
				pupresponse[condition][i] = pyenalysis.hampel(pupresponse[condition][i])
				# proportionalize
				traces[condition].append(pupresponse[condition][i] / numpy.median(baseline[condition][i]))
				baseline[condition][i] = baseline[condition][i] / numpy.median(baseline[condition][i])
			
		## DEBUG #
		#for condition in traces.keys():
		#	for i in range(len(traces[condition])):
		#		pyplot.plot(traces[condition][i])
		#pyplot.show()
		## # # # #
		
		# AVERAGE CONDITIONS
		avgtraces = {}
		stdtraces = {}
		semtraces = {}
		for condition in traces.keys():
			avgtraces[condition] = nanmean(traces[condition], axis=0)
			stdtraces[condition] = nanstd(traces[condition], axis=0)
			semtraces[condition] = stdtraces[condition] / (len(traces[condition])**0.5)
		
		# AVERAGE BASELINE
		baseavgtraces = {}
		basestdtraces = {}
		basesemtraces = {}
		for condition in traces.keys():
			baseavgtraces[condition] = nanmean(baseline[condition], axis=0)
			basestdtraces[condition] = nanstd(baseline[condition], axis=0)
			basesemtraces[condition] = basestdtraces[condition] / (len(baseline[condition])**0.5)
		
		# STATS
		ttrace, ptrace = ttest_rel(traces['black'], traces['white'], axis=0)
		
		# PLOT
		# open new figure
		fig, ax = pyplot.subplots(nrows=1, ncols=1)
		fig.set_dpi(DPI)
		fig.set_size_inches(FIGSIZE, forward=True)
		# loop through conditions
		for condition in avgtraces.keys():
			# draw baseline
			ax.plot(basepuptime, baseavgtraces[condition], '-', c=PLOTCOLS[condition])
			# fill SEM area
			y1 = baseavgtraces[condition] + basesemtraces[condition]
			y2 = baseavgtraces[condition] - basesemtraces[condition]
			ax.fill_between(basepuptime, y1, y2, color=PLOTCOLS[condition], alpha=0.3)
			# draw stimulus onset
			baseonset = numpy.arange(basepuptime[-1],basepuptime[-1]+16)
			ax.fill_between(baseonset, numpy.ones(len(baseonset))*PUPAXES[2], numpy.ones(len(baseonset))*PUPAXES[3], color=PLOTCOLS['pupscreenonset'], alpha=0.2)
			# draw trace
			ax.plot(puptime, avgtraces[condition], '-', c=PLOTCOLS[condition], label=condition)
			# fill SEM area
			y1 = avgtraces[condition] + semtraces[condition]
			y2 = avgtraces[condition] - semtraces[condition]
			ax.fill_between(puptime, y1, y2, color=PLOTCOLS[condition], alpha=0.3)
		# fill significantly different area
		ax.fill_between(puptime, numpy.ones(len(puptime))*PUPAXES[2], numpy.ones(len(puptime))*PUPAXES[3], where=ptrace<PUPALPHA, color=PLOTCOLS['significant'], alpha=0.2)
		# finish plot
		ax.axis(PUPAXES)
		ax.legend(loc='upper left')
		ax.set_xlabel("time (ms)")
		ax.set_ylabel("pupil size (proportional change)")
		# save plot
		fig.savefig(os.path.join(outputdir, "pupilometry.png"))
		# close figure
		pyplot.close(fig)


	# # # # #
	# SACCADES
	
	if DOSACCADES:
	
		# READ DATA
		saccdata = read_data[trackertype](DATAFILE, "target_on", stop="target_fixated", missing=0.0, debug=False)
		indices = {'starting error':[], 'landing error':[], 'amplitude':[], 'duration':[], 'curvature':[], 'mean velocity':[], 'peak velocity':[]}
		
		# NEW FIGURES
		# empty dicts
		fig = {'vel':None, 'traject':None}; ax = {'vel':None, 'traject':None}
		for t in ['vel', 'traject']:
			fig[t], ax[t] = pyplot.subplots(nrows=1, ncols=1)
			fig[t].set_dpi(DPI)
			fig[t].set_size_inches(FIGSIZE, forward=True)
		
		# PARSE DATA
		for i in range(len(saccdata)):
			
			# INTER-SAMPLE MEASURES
			# the distance between samples is the square root of the sum
			# of the squared horizontal and vertical interdistances
			intdist = (numpy.diff(saccdata[i]['x'])**2 + numpy.diff(saccdata[i]['y'])**2)**0.5
			# recalculate the distances from pixels to cm to visual angle
			intdist = cm2ang(intdist/PIXPERCM, SCREENDIST)
			# get inter-sample times
			inttime = numpy.diff(saccdata[i]['trackertime'])
			# recalculate inter-sample times to seconds
			inttime = inttime / 1000.0
			
			# VELOCITY AND ACCELERATION
			# the velocity between samples is the inter-sample distance
			# divided by the inter-sample time
			vel = intdist / inttime
			# the acceleration is the sample-to-sample difference in
			# eye movement velocity
			acc = numpy.diff(vel)

#			# SACCADE DETECTION - DISPERSION (UNUSED)
#			# saccade start position
#			sx = FIXPOS[0] + ang2cm(MAXDISP, SCREENDIST)*PIXPERCM
#			# saccade end position
#			ex = TARPOS[0] - ang2cm(MAXENDERR, SCREENDIST)*PIXPERCM
#			# find first sample of saccade
#			# (the one just before passing the dispersion border)
#			t1i = numpy.where(saccdata[i]['x'] > sx)[0][0] - 1
#			t2i = numpy.where(saccdata[i]['x'] > ex)[0][0] + 1

			# SACCADE DETECTION - VELOCITY
			# ignore saccades that did not last long enough
			j = 0
			dur = 0
			thereisasaccade = True
			while dur < MINSACDUR:
				# saccade start (t1) is when the velocity or acceleration
				# surpass threshold, saccade end (t2) is when both return
				# under threshold
				try:
					t1i = numpy.where((vel[1:] > VELTHRESH).astype(int) + (acc > ACCTHRESH).astype(int) >= 1)[0][j] + 1
					t2i = numpy.where((vel[1+t1i:] < VELTHRESH).astype(int) + (acc[t1i:] < ACCTHRESH).astype(int) == 2)[0][0] + 1 + t1i + 2
				except IndexError:
					thereisasaccade = False
					break
				
				# TIME STAMPS
				t1 = saccdata[i]['trackertime'][t1i]
				t2 = saccdata[i]['trackertime'][t2i]
				dur = t2 - t1
				j += 1
			
			# PLOT INDIVIDUAL TRACES
			if thereisasaccade:
				# velocity profile
				ax['vel'].plot(saccdata[i]['time'][t1i:t2i]-saccdata[i]['time'][t1i], vel[t1i-1:t2i-1], c=PLOTCOLS[trackertype], alpha=0.5)
				# trajectory
				x = saccdata[i]['x'][t1i:t2i]
				y = saccdata[i]['y'][t1i:t2i] # - saccdata[i]['y'][t1i] # (uncomment to correct starting position)
				x = cm2ang(x/PIXPERCM, SCREENDIST)
				y = cm2ang(y/PIXPERCM, SCREENDIST)
				ax['traject'].plot(x, y, '-', c=PLOTCOLS[trackertype])
				
				# INDICES
				indices['starting error'].append(cm2ang((((saccdata[i]['x'][t1i] - FIXPOS[0])**2 + (saccdata[i]['y'][t1i] - FIXPOS[1])**2)**0.5)/PIXPERCM, SCREENDIST))
				indices['landing error'].append(cm2ang((((saccdata[i]['x'][t2i] - TARPOS[0])**2 + (saccdata[i]['y'][t2i] - TARPOS[1])**2)**0.5)/PIXPERCM, SCREENDIST))
				# correct y for starting position
				x = cm2ang(saccdata[i]['x'][t1i:t2i] / PIXPERCM, SCREENDIST)
				y = cm2ang((saccdata[i]['y'][t1i:t2i] - saccdata[i]['y'][t1i]) / PIXPERCM, SCREENDIST)
				# correct y for slope between starting and ending point
				x = x - x[0]
				slope = (y[-1] - y[0]) / len(y)
				y = y - (slope * x)
				# curvature
				indices['curvature'].append(numpy.max(y))
				# amplitude
				indices['amplitude'].append(cm2ang((((saccdata[i]['x'][t1i] - saccdata[i]['x'][t2i])**2 + (saccdata[i]['y'][t1i] - saccdata[i]['y'][t2i])**2)**0.5)/PIXPERCM, SCREENDIST))
				# duration
				indices['duration'].append(dur)
				# mean velocity
				indices['mean velocity'].append(numpy.mean(vel))
				# peak velocity
				indices['peak velocity'].append(numpy.max(vel))
		
		# SAVE INDICES
		# open new text document
		txtfile = open(os.path.join(outputdir, "saccadometry_indices.txt"), 'w')
		# calculate data
		header = ['']
		content = {'M':['M'],'SD':['SD']}
		for k in indices.keys():
			header.append(k)
			content['M'].append(numpy.mean(indices[k]))
			content['SD'].append(numpy.std(indices[k]))
		# write data
		txtfile.write(OUTSEP.join(header) + '\n')
		txtfile.write(OUTSEP.join(map(str, content['M'])) + '\n')
		txtfile.write(OUTSEP.join(map(str, content['SD'])) + '\n')
		# close textfile
		txtfile.close()
		
		# SAVE FIGURE
		for t in ['vel', 'traject']:
			# finish plot
			ax[t].legend()
			if t == 'vel':
				# axis
				ax[t].set_xlim([0, 70])
				ax[t].set_ylim([0, 1000])
				# axis labels
				ax[t].set_xlabel("time since saccade onset (ms)")
				ax[t].set_ylabel("gaze velocity (degrees of VA per square second)")
			elif t == 'traject':
				# draw targets
				ms = (cm2ang(12/PIXPERCM, SCREENDIST) / (16-12)) * (FIGSIZE[1]*DPI)
				ax[t].plot(cm2ang(FIXPOS[0]/PIXPERCM, SCREENDIST), cm2ang(FIXPOS[1]/PIXPERCM, SCREENDIST), '+', markersize=ms, c=PLOTCOLS['validation'], alpha=0.5, markeredgewidth=3)
				ax[t].plot(cm2ang(TARPOS[0]/PIXPERCM, SCREENDIST), cm2ang(TARPOS[1]/PIXPERCM, SCREENDIST), 'o', markersize=ms, c=PLOTCOLS['validation'], alpha=0.5, markeredgewidth=0)
#				# DEBUG #
#				# upper and lower bound of stimulus at actual height
#				x = numpy.arange(0, cm2ang(DISPSIZE[0]/PIXPERCM, SCREENDIST), 1)
#				ax[t].plot(x, numpy.ones(len(x)) * cm2ang((DISPSIZE[1]*0.5)/PIXPERCM, SCREENDIST) - cm2ang(12/PIXPERCM, SCREENDIST), '-')
#				ax[t].plot(x, numpy.ones(len(x)) * cm2ang((DISPSIZE[1]*0.5)/PIXPERCM, SCREENDIST) + cm2ang(12/PIXPERCM, SCREENDIST), '-')
#				# # # # #
				# axis
				ax[t].set_xlim([0, cm2ang(DISPSIZE[0]/PIXPERCM, SCREENDIST)])
				#ax[t].set_ylim([0, cm2ang(DISPSIZE[1]/PIXPERCM, SCREENDIST)])
				ax[t].set_ylim([12, 16])
				# axis labels
				ax[t].set_xlabel("horizontal position (degrees of VA)")
				ax[t].set_ylabel("vertical position (degrees of VA)")
			# save plot
			fig[t].savefig(os.path.join(outputdir, "saccadometry_%s.png" % t))
			# close figure
			pyplot.close(fig[t])


	# # # # #
	# INTER-SAMPLE TIME
	
	if DOINTSAMPLETIME:
	
		# get all samples
		if trackertype == 'eyetribe':
			startcode = "start_recording"
			endcode = "stop_recording"
		elif trackertype == "eyelink":
			startcode = "RECORD"
			endcode = None
		allsamples = read_data[trackertype](DATAFILE, startcode, stop=endcode, missing=0.0, debug=False)
		
		# empty list to contain all inter-sample times and coordinate sums
		total = 0
		allinttimes = []
		combined = []
		
		# loop through all recordings
		for i in range(len(allsamples)):
			# update total
			total += len(allsamples[i]['trackertime'])
			# get inter-sample times
			inttime = numpy.diff(allsamples[i]['trackertime'])
			# add to total
			allinttimes.extend(list(inttime))
			# combined x and y
			combined.extend(list(allsamples[i]['x']+allsamples[i]['y']))
		
		# list to array
		ait = numpy.array(allinttimes)
		itotal = len(ait)
		combined = numpy.array(combined)
		
		if trackertype == 'eyetribe':
			# 16.67 ms inter-sample time (60 Hz)
			N16 = numpy.sum((14.67 < ait).astype(int) + (ait <= 18.67).astype(int) == 2)
			# 33.33 ms inter-sample time (30 Hz)
			N33 = numpy.sum((20.67 < ait).astype(int) + (ait <= 35).astype(int) == 2)
			# 50 ms inter-sample time (20 Hz)
			N50 = numpy.sum((35 < ait).astype(int) + (ait <= 50).astype(int) == 2)
			# 0 ms (inf Hz)
			Nlower = numpy.sum((0 <= ait).astype(int) + (ait <= 12.67).astype(int) == 2)
			# over 50 ms
			Nhigher = numpy.sum((50 < ait).astype(int))
			# all missing data
			Nmissing = numpy.sum((combined == 0.0).astype(int))

			# open new text document
			txtfile = open(os.path.join(outputdir, "intersample_times.txt"), 'w')
			# calculate data
			header = ['intersample time', '0-15', '16', '19-35', '35-50', 'higher', 'inttimes_total', 'samples_missing', 'samples_total']
			content = ['', Nlower, N16, N33, N50, Nhigher, itotal, Nmissing, total]
			# write data
			txtfile.write(OUTSEP.join(header) + '\n')
			txtfile.write(OUTSEP.join(map(str, content)) + '\n')
			# close textfile
			txtfile.close()

		elif trackertype == 'eyelink':
			# 0 ms
			N0 = numpy.sum((0.0 == ait).astype(int))
			# 1 ms
			N1 = numpy.sum((1.0 == ait).astype(int))
			# 2 ms
			N2 = numpy.sum((2.0 == ait).astype(int))
			# 3 ms
			N3 = numpy.sum((3.0 == ait).astype(int))
			# higher
			Nh = numpy.sum((3.0 < ait).astype(int))
			# all missing data
			Nmissing = numpy.sum((combined == 0.0).astype(int))

			# open new text document
			txtfile = open(os.path.join(outputdir, "intersample_times.txt"), 'w')
			# calculate data
			header = ['intersample time', '0', '1', '2', '3', 'higher', 'inttimes_total', 'samples_missing', 'samples_total']
			content = ['', N0, N1, N2, N3, Nh, itotal, Nmissing, total]
			# write data
			txtfile.write(OUTSEP.join(header) + '\n')
			txtfile.write(OUTSEP.join(map(str, content)) + '\n')
			# close textfile
			txtfile.close()


# # # # #
# CLOSE

# finish overall validation plot
if DOVALIDATION:
	# finish overall figure
	soax.axis([0, DISPSIZE[0], 0, DISPSIZE[1]])
	soax.invert_yaxis()
#	soax.legend()
	soax.set_xlabel("display x coordinate (pixels)")
	soax.set_ylabel("display y coordinate (pixels)")
	# save plot
	sofig.savefig(os.path.join(OUTDIR, "validationpoint_all.png"))
	# close figure
	pyplot.close(sofig)
