# Load a trial handler and
# create an associated table in the iohub data file
#
from psychopy.data import TrialHandler,importConditions

from psychopy.iohub import launchHubServer

# Start the ioHub process. The return variable is what is used
# during the experiment to control the iohub process itself,
# as well as any running iohub devices.
io=launchHubServer()

exp_conditions=importConditions('trialTypes.xlsx')
trials = TrialHandler(exp_conditions,1)

# Inform the ioHub server about the TrialHandler
#
io.createTrialHandlerRecordTable(trials)

# Read a row of the trial handler for
# each trial of your experiment
#
for trial in trials:
    print trial
    # do whatever...


# During the trial, trial variable values can be updated
#
#trial['TRIAL_START']=flip_time

# At the end of each trial, before getting
# the next trial handler row, send the trial
# variable states to iohub so they can be stored for future
# reference.
#
io.addTrialHandlerRecord(trial.values())