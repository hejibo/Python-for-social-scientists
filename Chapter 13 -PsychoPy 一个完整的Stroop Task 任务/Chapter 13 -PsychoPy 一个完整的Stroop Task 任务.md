# 第13章 -PsychoPy 一个完整的Stroop Task 任务

作者： 何吉波博士，优视眼动科技公司创始人，hejibo@usee.tech, [http://www.usee.tech](http://www.usee.tech)  

Stroop Task可能是认知心理学中最广为人知的一个任务了。 下面， 我们将通过演示如何逐步实现Stroop Task来向读者朋友们介绍， 如何用PsychoPy来编写一个完全的实验程序。一个实验程序通常包括下面这几个代码模块。 
1. 预先准备实验刺激和实验全局变量
2. 实验指导语呈现
3. 实验刺激呈现
4. 被试反应数据的记录
5. 实验结束语呈现
6. 实验数据结果记录
下面，我们将分别讲解以上六个模块，然后拼结成一个完成的Stroop Task实验程序。

## 1. 预先准备实验刺激和实验全局变量

```python
# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=5, method='random', 
    extraInfo=expInfo, originPath=None,
    trialList=data.importConditions(u'conditions.xlsx'),
    seed=None, name='trials')
thisExp.addLoop(trials)  # add the loop to the experiment
```

## 2. 实验指导语呈现
    我们在第11章的“1.4 呈现多行富文本 (Rich Text)”小节已经详细地介绍了如何呈现多行文字，我们很容易将它修改为实验指导语。下面的代码是我们的实验指导语呈现代码。 

```python
#!/usr/bin/env python2
from psychopy import visual, core, event

#create a window to draw in
myWin = visual.Window((800.0,800.0))
myWin.setRecordFrameIntervals()


#INITIALISE SOME STIMULI
instruction = visual.TextStim(myWin, color='#FFFFFF',
                        text = u'''         Instruction
                        
This is an experiment instruction. You need to do the following stuff.
1. Fixate at the dot.
2. press the 'Y' or 'N' key 
Press any key to continue''',
                        units='norm', height=0.1,
                        pos=[0, 0.6], alignHoriz='center',alignVert='top'
                       )
instruction.draw()
    
myWin.flip()

#pause, so you get a chance to see it!
core.wait(5.0)

```
## 3. 实验刺激呈现

```python
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
```     

## 4. 被试反应数据的记录


```python
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
```

## 5. 实验结束语呈现
    实验结束语和实验指导语类似，只是呈现的文本内容不相同。我们可以很容易地将本章的第“2. 实验指导语呈现”小节个性为实验结束语。下面的代码是我们的实验结束语呈现的代码。 
```python
#!/usr/bin/env python2
from psychopy import visual, core, event

#create a window to draw in
myWin = visual.Window((800.0,800.0))
myWin.setRecordFrameIntervals()


#INITIALISE SOME STIMULI
instruction = visual.TextStim(myWin, color='#FFFFFF',
                        text = u'''         Instruction
                        
Thank you! This is the end of the study.
Press any key to continue''',
                        units='norm', height=0.1,
                        pos=[0, 0.6], alignHoriz='center',alignVert='top'
                       )
instruction.draw()
    
myWin.flip()

#pause, so you get a chance to see it!
core.wait(5.0)

```

## 6. 实验数据结果记录
