## 使用uSeeEyeTracker进行眼动试验

1. 安装Python开发运行环境

我们的试验需要安装Python 2.7运行环境，Windows操作系统的 Python 2.7 下载地址是：  
https://www.python.org/ftp/python/2.7.14/python-2.7.14.msi  
在后面的示例中，我们的Python安装路径是 C:\Python27 。

2. 安装useeeyelib

useeeyelib使我们专门为uSeeEyeTracker开发的Python程序库，可以从uSEE的官网下载。  
下载地址：  
http://www.usee.tech/dev/files/useeeyelib-0.1-py2-none-any.whl   
或者：  
http://owncloud.learndevops.cn/tmp/usee/useeeyelib-0.1-py2-none-any.whl  
执行安装命令： c:\Python27\Scripts\pip.exe install useeeyelib-0.1-py2-none-any.whl  

安装完成后，我们可以通过import useeeyelib来测试安装是否成功。

![image](http://owncloud.learndevops.cn/tmp/usee/useeeyelib_doc_screenshot/install_useeeyelib.png)

3. 安装 pygame

执行命令：c:\Python27\Scripts\pip.exe install pygame  
安装完成后，我们可以通过import pygame来测试安装是否成功。  

![image](http://owncloud.learndevops.cn/tmp/usee/useeeyelib_doc_screenshot/install_pygame.png)

4. 安装 matplotlib

执行命令：c:\Python27\Scripts\pip.exe install matplotlib  
安装完成后，我们可以通过import matplotlib。  
补充图片： install_matplotlib.png  

![image](http://owncloud.learndevops.cn/tmp/usee/useeeyelib_doc_screenshot/install_matplotlib.png)

5. 安装 Pillow

执行命令：c:\Python27\Scripts\pip.exe install pillow  
安装完成后，我们可以通过from PIL import Image 来测试安装是否成功。  

![image](http://owncloud.learndevops.cn/tmp/usee/useeeyelib_doc_screenshot/install_pillow.png)

6. 下载测试代码

大家可以从uSEE官网下载我们提供的测试代码。地址：  
http://www.usee.tech/dev/files/useeeyelib_example.zip  
或者  
http://owncloud.learndevops.cn/tmp/usee/useeeyelib_example.zip  
下载后将文件解压缩。  

![image](http://owncloud.learndevops.cn/tmp/usee/useeeyelib_doc_screenshot/example_files.png)

7. 修改测试代码参数

测试代码中有两个主要的程序，第一个是 experiment.py，这个是用来采集数据的程序。  
另外一个是 analysis.py，这个是用来分析数据的程序。  
在进行测试之前，我们需要根据电脑屏幕的分辨率来修改程序中的RESOLUTION参数。  
笔者用来测试的电脑屏幕分辨率是1600x900。以下的示例都是以此分辨率进行的测试。
需要修改的代码截图如下：

![image](http://owncloud.learndevops.cn/tmp/usee/useeeyelib_doc_screenshot/modify_experiment_screen_resolution.png)

![image](http://owncloud.learndevops.cn/tmp/usee/useeeyelib_doc_screenshot/modify_analysis_screen_resolution.png)

8. 运行测试代码

运行测试代码之前，要启动uSee Server程序，并完成Calibration操作。  
首先运行 c:\Python27\python.exe  experiment.py 。  
此时程序会显示imgs文件夹下面的图片，同时程序会采集Eye Tracker的数据，记录被试人员注视的位置数据。  

![image](http://owncloud.learndevops.cn/tmp/usee/useeeyelib_doc_screenshot/run_expriment.png)

experiment.py 程序运行完毕后，会在当前目录生成一个数据文件 example_data.txt.tsv 。  
这里面记录了采集到的Eye Tracker数据。  

![image](http://owncloud.learndevops.cn/tmp/usee/useeeyelib_doc_screenshot/example_data.png)

9. 运行分析程序

然后我们运行 c:\Python27\python.exe  analysis.py 。  

![image](http://owncloud.learndevops.cn/tmp/usee/useeeyelib_doc_screenshot/run_analysis.png)

此时程序会根据采集到的数据和原始图片，生成对应的分析结果图片。  
每张图片会有三个分析结果，分别是：samples fixations heatmap 。

![image](http://owncloud.learndevops.cn/tmp/usee/useeeyelib_doc_screenshot/example_output.png)

现在我们可以查看分析结果了：

![image](http://owncloud.learndevops.cn/tmp/usee/useeeyelib_example/output/advertisment_samples.png)

![image](http://owncloud.learndevops.cn/tmp/usee/useeeyelib_example/output/advertisment_heatmap.png)

![image](http://owncloud.learndevops.cn/tmp/usee/useeeyelib_example/output/advertisment_fixations.png)

