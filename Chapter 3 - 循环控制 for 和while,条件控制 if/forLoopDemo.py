'''
forLoopDemo.py 
demostrate the for loop and the importance of indention.

'''
import numpy
data = {}
data['subject-1'] = {'RT':[300, 256, 35], 'acc':[1, 1, 0]}
data['subject-2'] = {'RT':[400, 512, 100009], 'acc':[1, 0, 1]}
data['subject-3'] = {'RT':[732, 542, 839], 'acc':[1, 1, 1]}
print data

# find all subject data information using the for loop.
RTList = []
for subjectID in data.keys():
    print data[subjectID]["RT"]
    RTList.extend(data[subjectID]["RT"])

# calculate mean and std at group level. This is only calculated once as it is out of the indention level of the for group.
print "mean and standard deviation of RT:",numpy.mean(RTList),numpy.std(RTList)

print "-----------section separator--------------"
# demostrate indention is part of the grammar of Python
RTListIndividual = []
for subjectID in data.keys():
    print data[subjectID]["RT"]
    RTListIndividual.extend(data[subjectID]["RT"])
    # calculate mean and std at individual participant level.This is calculated three times as it is within the same indention level of the for group.
    print "mean and standard deviation of RT:", numpy.mean(RTListIndividual),numpy.std(RTListIndividual)