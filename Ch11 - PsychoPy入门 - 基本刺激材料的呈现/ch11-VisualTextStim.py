#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#使用from psychopy import visual导入visual这个视觉库
from psychopy import visual, core, event

#定义一个取名为myWin的画布
myWin = visual.Window((300.0,300.0))
myWin.setRecordFrameIntervals()

#使用visual.TextStim函数定义要呈现的文本信息
psychopyTxt = visual.TextStim(myWin, color='#FFFFFF',
                        text = u"PsychoPy is a GREAT tool",
                        units='norm', height=0.1,
                        pos=[0.5, 0.5], alignHoriz='right',alignVert='top')

#通过psychopyTxt.draw()这个绘制函数讲文本信息绘制到myWin画布
psychopyTxt.draw()
    
myWin.flip()

#让文本信息停留五秒钟，否则呈现内容就会一闪而过
core.wait(5.0)