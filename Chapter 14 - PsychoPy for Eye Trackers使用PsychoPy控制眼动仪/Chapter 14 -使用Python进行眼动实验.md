# 第14章  - 使用Python进行眼动实验

作者： 孟光 和
何吉波博士，优视眼动科技公司创始人，hejibo@usee.tech, [http://www.usee.tech](http://www.usee.tech)  


## 1. 眼动仪和眼动的常见指标

The basics
When you look at an image, you will show (mostly) three types of eye movements: fixations, saccades, and blinks. Blinks happen when you close your eyelids and see nothing. Saccades occur when you quickly move your eyes. When you do, your vision is largely suppressed (if it wasn’t, you would see a blur during saccades). Fixations are the times when your eyes stay relatively still, and you can actually see what you are looking at.


## 2. 设备和材料要求
### 2.1. 软件环境要求
- Windows 10 操作系统。
- 完整的中文语言支持。
- 时间准确。
- 微软 .Net 4.5 Runtime。
- 屏幕显示无缩放。

### 2.2. 硬件环境要求
- 双核心CPU，2Ghz以上主频。
- 4GB以上内存。
- 至少3个USB 2.0接口。
- 21-24英寸显示器，分辨率高于1280x720。
- 20GB以上空闲存储空间。
- 标准键盘和鼠标。

## 3. 开发环境的搭建
### 3.1. 安装Python开发运行环境

我们的试验需要安装Python 2.7运行环境，Windows操作系统的 Python 2.7 下载地址是：  
https://www.python.org/ftp/python/2.7.14/python-2.7.14.msi  
在后面的示例中，我们的Python安装路径是 C:\Python27 。

### 3.2. 安装useeeyelib

useeeyelib使我们专门为uSeeEyeTracker开发的Python程序库，可以从uSEE的官网下载。  
下载地址：  
http://www.usee.tech/dev/files/useeeyelib-0.1-py2-none-any.whl   
或者：  
http://owncloud.learndevops.cn/tmp/usee/useeeyelib-0.1-py2-none-any.whl  
执行安装命令： c:\Python27\Scripts\pip.exe install useeeyelib-0.1-py2-none-any.whl  

安装完成后，我们可以通过import useeeyelib来测试安装是否成功。

![image](http://owncloud.learndevops.cn/tmp/usee/useeeyelib_doc_screenshot/install_useeeyelib.png)

### 3.3. 安装 pygame

执行命令：c:\Python27\Scripts\pip.exe install pygame  
安装完成后，我们可以通过import pygame来测试安装是否成功。  

![image](http://owncloud.learndevops.cn/tmp/usee/useeeyelib_doc_screenshot/install_pygame.png)

### 3.4. 安装 matplotlib

执行命令：c:\Python27\Scripts\pip.exe install matplotlib  
安装完成后，我们可以通过import matplotlib。  
补充图片： install_matplotlib.png  

![image](http://owncloud.learndevops.cn/tmp/usee/useeeyelib_doc_screenshot/install_matplotlib.png)

### 3.5. 安装 Pillow

执行命令：c:\Python27\Scripts\pip.exe install pillow  
安装完成后，我们可以通过from PIL import Image 来测试安装是否成功。  

![image](http://owncloud.learndevops.cn/tmp/usee/useeeyelib_doc_screenshot/install_pillow.png)

## 4. 开发刺激呈现程序 Experiment,py

## 5. 记录眼动仪数据和实际操作

### 5.1. 下载 uSee Server软件包

uSEE Server 20170928版本打包下载地址如下：  
链接：http://pan.baidu.com/s/1i5lBS1n 密码：5kr1  
解压缩下载到的 uSeeServer-20170928.zip 压缩包。

![image](http://owncloud.learndevops.cn/tmp/usee/useeserver_doc_screenshot/extract_install_package.png)

### 5.2. 接入 uSee Eye Tracker

将uSee Eye Tracker插入到电脑USB接口，并确认电脑已经正确识别设备。

### 5.3. 运行 uSee Server

双击运行 start.bat 来启动uSee Server。  

### 5.4. 设置 uSee Server

设置眼动仪模式为远程双目，关闭Glint闪光检测（默认已经设置为关闭）。  

![image](http://owncloud.learndevops.cn/tmp/usee/useeserver_doc_screenshot/set_usee_server.png)

### 5.5. 进行校准

将眼睛对准uSee Eye Tracker，使得uSee Server能够准确识别到眼睛瞳孔位置。  
然后点击 校准 按钮，开始进行校准操作。  
在校准操作过程中，被试者的目光要追随电脑屏幕的光标。  
校准结束后，可以根据实际情况接受校准结果或者重新进行校准操作。  

![image](http://owncloud.learndevops.cn/tmp/usee/useeserver_doc_screenshot/start_calibration.png)

### 5.6. 运行实验代码

运行测试代码之前，要启动uSee Server程序，并完成Calibration操作。  
首先运行 c:\Python27\python.exe  experiment.py 。  
此时程序会显示imgs文件夹下面的图片，同时程序会采集Eye Tracker的数据，记录被试人员注视的位置数据。  

![image](http://owncloud.learndevops.cn/tmp/usee/useeeyelib_doc_screenshot/run_expriment.png)

experiment.py 程序运行完毕后，会在当前目录生成一个数据文件 example_data.txt.tsv 。  
这里面记录了采集到的Eye Tracker数据。  

![image](http://owncloud.learndevops.cn/tmp/usee/useeeyelib_doc_screenshot/example_data.png)

## 6. 分析眼动数据

然后我们运行 c:\Python27\python.exe  analysis.py 。  

![image](http://owncloud.learndevops.cn/tmp/usee/useeeyelib_doc_screenshot/run_analysis.png)

此时程序会根据采集到的数据和原始图片，生成对应的分析结果图片。  
每张图片会有三个分析结果，分别是：samples fixations heatmap 。

![image](http://owncloud.learndevops.cn/tmp/usee/useeeyelib_doc_screenshot/example_output.png)

现在我们可以查看分析结果了：

![image](http://owncloud.learndevops.cn/tmp/usee/useeeyelib_example/output/advertisment_samples.png)

![image](http://owncloud.learndevops.cn/tmp/usee/useeeyelib_example/output/advertisment_heatmap.png)

![image](http://owncloud.learndevops.cn/tmp/usee/useeeyelib_example/output/advertisment_fixations.png)

