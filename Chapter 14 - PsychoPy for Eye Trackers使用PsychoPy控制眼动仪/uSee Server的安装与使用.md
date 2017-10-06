## uSee Server的安装与使用

1. 软件环境要求
- Windows 10 操作系统。
- 完整的中文语言支持。
- 时间准确。
- 微软 .Net 4.5 Runtime。
- 屏幕显示无缩放。

2. 硬件环境要求
- 双核心CPU，2Ghz以上主频。
- 4GB以上内存。
- 至少3个USB 2.0接口。
- 21-24英寸显示器，分辨率高于1280x720。
- 20GB以上空闲存储空间。
- 标准键盘和鼠标。

3. 下载 uSee Server软件包

uSEE Server 20170928版本打包下载地址如下：  
链接：http://pan.baidu.com/s/1i5lBS1n 密码：5kr1  
解压缩下载到的 uSeeServer-20170928.zip 压缩包。

![image](http://owncloud.learndevops.cn/tmp/usee/useeserver_doc_screenshot/extract_install_package.png)

4. 接入 uSee Eye Tracker

将uSee Eye Tracker插入到电脑USB接口，并确认电脑已经正确识别设备。

5. 运行 uSee Server

双击运行 start.bat 来启动uSee Server。  

6. 设置 uSee Server

设置眼动仪模式为远程双目，关闭Glint闪光检测（默认已经设置为关闭）。  

![image](http://owncloud.learndevops.cn/tmp/usee/useeserver_doc_screenshot/set_usee_server.png)

7. 进行校准

将眼睛对准uSee Eye Tracker，使得uSee Server能够准确识别到眼睛瞳孔位置。  
然后点击 校准 按钮，开始进行校准操作。  
在校准操作过程中，被试者的目光要追随电脑屏幕的光标。  
校准结束后，可以根据实际情况接受校准结果或者重新进行校准操作。  

![image](http://owncloud.learndevops.cn/tmp/usee/useeserver_doc_screenshot/start_calibration.png)

8. 运行其他数据采集程序

以上步骤操作完成后，就可以运行其他数据采集程序进行数据收集和分析了。

