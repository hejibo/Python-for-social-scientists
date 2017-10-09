import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=5, method='random', 
    extraInfo=expInfo, originPath=None,
    trialList=data.importConditions(u'conditions.xlsx'),
    seed=None, name='trials')
    
print "----------------trials:",trials

thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial.keys():
        exec(paramName + '= thisTrial.' + paramName)

for thisTrial in trials:
    currentLoop = trials
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial.' + paramName)
    
    #------Prepare to start Routine "trial"-------
    t = 0
    trialClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    target.setColor(colour, colorSpace='rgb')
    target.setText(word)
    Response = event.BuilderKeyResponse()  # create an object of type KeyResponse
    Response.status = NOT_STARTED
    # keep track of which components have finished
    trialComponents = []
    trialComponents.append(ISI)
    trialComponents.append(target)
    trialComponents.append(Response)
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "trial"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *target* updates
        if t >= 0.5 and target.status == NOT_STARTED:
            # keep track of start time/frame for later
            target.tStart = t  # underestimates by a little under one frame
            target.frameNStart = frameN  # exact frame index
            target.setAutoDraw(True)
        if target.status == STARTED and t >= (0.5 + (5-win.monitorFramePeriod*0.75)): #most of one frame period left
            target.setAutoDraw(False)
        
        # *Response* updates
        if t >= 0.5 and Response.status == NOT_STARTED:
            # keep track of start time/frame for later
            Response.tStart = t  # underestimates by a little under one frame
            Response.frameNStart = frameN  # exact frame index
            Response.status = STARTED
            # keyboard checking is just starting
            Response.clock.reset()  # now t=0
            event.clearEvents(eventType='keyboard')
        if Response.status == STARTED:
            theseKeys = event.getKeys(keyList=['a', 's', 'd', 'f'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                Response.keys = theseKeys[-1]  # just the last key pressed
                Response.rt = Response.clock.getTime()
                # was this 'correct'?
                if (Response.keys == str(corrAns)) or (Response.keys == corrAns):
                    Response.corr = 1
                else:
                    Response.corr = 0
                # a response ends the routine
                continueRoutine = False
        # *ISI* period
        if t >= 0.0 and ISI.status == NOT_STARTED:
            # keep track of start time/frame for later
            ISI.tStart = t  # underestimates by a little under one frame
            ISI.frameNStart = frameN  # exact frame index
            ISI.start(0.5)
        elif ISI.status == STARTED: #one frame should pass before updating params and completing
            ISI.complete() #finish the static period
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if Response.keys in ['', [], None]:  # No response was made
       Response.keys=None
       # was no response the correct answer?!
       if str(corrAns).lower() == 'none': Response.corr = 1  # correct non-response
       else: Response.corr = 0  # failed to respond (incorrectly)
    # store data for trials (TrialHandler)
    trials.addData('Response.keys',Response.keys)
    trials.addData('Response.corr', Response.corr)
    if Response.keys != None:  # we had a response
        trials.addData('Response.rt', Response.rt)
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 5 repeats of 'trials'

win.close()
core.quit()