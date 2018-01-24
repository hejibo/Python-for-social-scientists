'''
ifBreakDemo.py
demostrate the while loop, and exit using if break conditional.
'''
import numpy
data = {}
data['subject-1'] = {'RT':[300, 256, 35], 'acc':[1, 1, 0]}
data['subject-2'] = {'RT':[400, 512, 100009], 'acc':[1, 0, 1]}
data['subject-3'] = {'RT':[732, 542, 839], 'acc':[1, 1, 1]}
print data

# find all subject data information using the for loop.
subjectIndex=1
RTList = []
while True:
    if subjectIndex>3:break
    key = 'subject-%d'%subjectIndex
    print data[key]["RT"]
    RTList.extend(data[key]["RT"])
    subjectIndex=subjectIndex+1

# calculate mean and std at group level. This is only calculated once as it is out of the indention level of the for group.
print "mean and standard deviation of RT:",numpy.mean(RTList),numpy.std(RTList)
