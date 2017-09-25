# -*- coding: utf-8 -*-
#!/usr/bin/env python2
'''
by 何吉波@优视眼动科技.
代码用于播放声音刺激。这个代码版可能只适用于Windows操作系统
'''
from psychopy import sound,core
tada = sound.Sound('tada.wav')
tada.play()
core.wait(2)
core.quit()