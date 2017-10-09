import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=5, method='random', 
    extraInfo=expInfo, originPath=None,
    trialList=data.importConditions(u'conditions.xlsx'),
    seed=None, name='trials')
    
print "----------------trials:",trials