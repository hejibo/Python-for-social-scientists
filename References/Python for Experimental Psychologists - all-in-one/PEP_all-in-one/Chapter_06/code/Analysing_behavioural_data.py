import os
import numpy
from matplotlib import pyplot
from scipy.stats import ttest_rel

# get the path to the current folder
DIR = os.path.dirname(os.path.abspath(__file__))
# construct the path to the data folder
DATADIR = os.path.join(DIR, 'data')

# construct a path to the output directory
OUTDIR = os.path.join(DIR, 'output')
# check if the output folder does not exist
if not os.path.isdir(OUTDIR):
    # only create an output directory if it doesn't exist yet
    os.mkdir(OUTDIR)

# construct a path to the individual output directory
IOUTDIR = os.path.join(OUTDIR, 'individual')
# check if the individual output folder exists
if not os.path.isdir(IOUTDIR):
    # create an individual output directory
    os.mkdir(IOUTDIR)

# define the number of participants
N = 10
# create an empty multi-dimensional array to store data
all_rt = numpy.zeros((2, 2, N))
all_acc = numpy.zeros((2, 2, N))

# loop through all participant numbers
for pnr in range(0, N):
    
    # construct the name of your data file
    datafile = os.path.join(DATADIR, 'pp%d.txt' % (pnr))
    
    # load the raw contents of the data file
    raw = numpy.loadtxt(datafile, dtype=str, unpack=True)
    
    # create new empty dict
    data = {}
    
    # loop through all vectors in raw
    for i in range(len(raw)):
        # the first index of each array is the variable name
        varname = raw[i][0]
        # try to convert the values to numbers
        try:
            values = raw[i][1:].astype(float)
        # if conversion to numbers fails, do not convert
        except:
            values = raw[i][1:]
        # create a new entry in the data dict
        # and make it hold the values
        data[varname] = values
    
    # make Boolean vectors for valid and invalid trials
    sel = {}
    sel['valid'] = data['valid'] == 1
    sel['invalid'] = data['valid'] == 0
    # make Boolean vectors for 100 and 900 ms SOAs
    sel[100] = data['soa'] == 100
    sel[900] = data['soa'] == 900
    
    # create an empty dict to hold descriptives
    descr = {}
    
    # loop through all SOAs
    for soa in [100, 900]:
        # create a new empty dict within the descr dict
        descr[soa] = {}
        # loop through all validities
        for val in ['valid', 'invalid']:
            # nest another empty dict within descr
            descr[soa][val] = {}
            # calculate statistics
            rt_m = numpy.median(data['RT'][sel[soa] & sel[val]])
            rt_sd = numpy.std(data['RT'][sel[soa] & sel[val]])
            rt_sem = rt_sd / numpy.sqrt(len(data['RT'][sel[soa] & sel[val]]))
            acc_m = numpy.mean(data['correct'][sel[soa] & sel[val]])
            # store the calculated values in descr
            descr[soa][val]['rt_m'] = rt_m
            descr[soa][val]['rt_sd'] = rt_sd
            descr[soa][val]['rt_sem'] = rt_sem
            descr[soa][val]['acc_m'] = acc_m
    
    # create a new figure with two subplots
    fig, (ax100, ax900) = pyplot.subplots(nrows=1, ncols=2, \
        sharey=True, figsize=(19.2, 10.8), dpi=100.0)
    
    # define the bar plot parameters
    width = 0.4
    intdist = 0.1
    # define the starting position (left edge) of the first bar
    barpos = 0.1
    
    # define the bar colours
    cols = {'valid':'#4e9a06', 'invalid':'#ce5c00'}
    
    for val in ['valid', 'invalid']:
        # draw the 100 ms SOA median reaction time
        ax100.bar(barpos, descr[100][val]['rt_m'], \
            width=width, yerr=descr[100][val]['rt_sem'], \
            color=cols[val], ecolor='black', label=val)
        # draw the 900 ms SOA median reaction time
        ax900.bar(barpos, descr[900][val]['rt_m'], \
            width=width, yerr=descr[900][val]['rt_sem'], \
            color=cols[val], ecolor='black', label=val)
        # update the bar position
        barpos += width + intdist
    
    # add y-axis label to the left plot
    ax100.set_ylabel('median reaction time (ms)')
    # add a legend to the right axis
    ax900.legend(loc='upper right')
    # hide x-axes
    ax100.get_xaxis().set_visible(False)
    ax900.get_xaxis().set_visible(False)
    # set x-axis limits
    ax100.set_xlim([0, barpos])
    ax900.set_xlim([0, barpos])
    # set y-axis limits
    ax100.set_ylim([100, 1000])
    ax900.set_ylim([100, 1000])
    # save the figure
    savefilename = os.path.join(IOUTDIR, \
        'reaction_times_%d.png' % (pnr))
    fig.savefig(savefilename)
    pyplot.close(fig)
    
    # store all median reaction times
    all_rt[0, 0, pnr] = descr[100]['valid']['rt_m']
    all_rt[1, 0, pnr] = descr[100]['invalid']['rt_m']
    all_rt[0, 1, pnr] = descr[900]['valid']['rt_m']
    all_rt[1, 1, pnr] = descr[900]['invalid']['rt_m']
    # store all proportion corrects
    all_acc[0, 0, pnr] = descr[100]['valid']['acc_m']
    all_acc[1, 0, pnr] = descr[100]['invalid']['acc_m']
    all_acc[0, 1, pnr] = descr[900]['valid']['acc_m']
    all_acc[1, 1, pnr] = descr[900]['invalid']['acc_m']

# create a new figure with a two subplots
fig, (rt_ax, acc_ax) = pyplot.subplots(nrows=2, \
    sharex=True, figsize=(19.2, 10.8), dpi=100.0)
# the x-axis will be the SOAs
x = [100, 900]
# the colours the valid and invalid conditions
cols = {'valid':'#4e9a06', 'invalid':'#ce5c00'}

# the y-axes will be the valid and invalid means
rt_valid = numpy.mean(all_rt[0, :, :], axis=1)
rt_invalid = numpy.mean(all_rt[1, :, :], axis=1)
# calculate the SEM (=SD/sqrt(N-1))
rt_valid_sem = numpy.std(all_rt[0,:,:], axis=1) \
    / numpy.sqrt(N - 1)
rt_invalid_sem = numpy.std(all_rt[1,:,:], axis=1) \
     / numpy.sqrt(N - 1)
# plot the means for valid and invalid as lines,
# including error bars for the standard error of the mean
rt_ax.errorbar(x, rt_valid, yerr=rt_valid_sem, \
    color=cols['valid'], ecolor='black', label='valid')
rt_ax.errorbar(x, rt_invalid, yerr=rt_invalid_sem, \
    color=cols['invalid'], ecolor='black', label='invalid')

# add y-axis label
rt_ax.set_ylabel('reaction time (ms)')
# add legend
rt_ax.legend(loc='upper right')

# calculate the accuracy means
acc_valid = numpy.mean(all_acc[0, :, :], axis=1)
acc_invalid = numpy.mean(all_acc[1, :, :], axis=1)
# calculate the SEM (=SD/sqrt(N-1))
acc_valid_sem = numpy.std(all_acc[0,:,:], axis=1) \
    / numpy.sqrt(N - 1)
acc_invalid_sem = numpy.std(all_acc[1,:,:], axis=1) \
    / numpy.sqrt(N - 1)
# plot the means for valid and invalid as lines,
# including error bars for the standard error of the mean
acc_ax.errorbar(x, acc_valid, yerr=acc_valid_sem, \
    color=cols['valid'], ecolor='black', label='valid')
acc_ax.errorbar(x, acc_invalid, yerr=acc_invalid_sem, \
    color=cols['invalid'], ecolor='black', label='invalid')

# add axis labels
acc_ax.set_xlabel('stimulus onset asynchrony (ms)')
acc_ax.set_ylabel('proportion correct')
# set x limits
acc_ax.set_xlim([0, 1000])
# save the figure as a PNG image
savefilename = os.path.join(OUTDIR, 'averages.png')
fig.savefig(savefilename)

# perform two related-samples t-test
t100, p100 = ttest_rel(all_rt[0,0,:], all_rt[1,0,:])
t900, p900 = ttest_rel(all_rt[0,1,:], all_rt[1,1,:])

print('\nstats report:')
print('SOA 100ms, valid vs invalid: t=%.2f, p=%.3f' % \
    (t100, p100))
print('SOA 900ms, valid vs invalid: t=%.2f, p=%.3f' % \
    (t900, p900))

t100, p100 = ttest_rel(all_acc[0,0,:], all_acc[1,0,:])
t900, p900 = ttest_rel(all_acc[0,1,:], all_acc[1,1,:])
print('SOA 100ms, valid vs invalid: t=%.2f, p=%.3f' % \
    (t100, p100))
print('SOA 900ms, valid vs invalid: t=%.2f, p=%.3f' % \
    (t900, p900))