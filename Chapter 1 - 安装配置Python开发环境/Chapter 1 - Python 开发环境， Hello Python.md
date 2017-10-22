# 第1章 - Python 开发环境， Hello Python

作者： 何吉波博士，优视眼动科技公司创始人，hejibo@usee.tech, [http://www.usee.tech](http://www.usee.tech)  

## 学习 Python 可以做什么？
大家在购买这本书，或者开始阅读时，一定会问：“为什么我需要学习Python？” 恭喜您，拿到此书时，您正在尝试着打开一扇门，可能带您进入一个全新的世界。 

与其告诉您为什么您应该学习 Python这样的营销行为。我觉得我首先更应该回答的是，我为什么能或者会成为一位科研人员，为什么这么热爱 Python，以致于来写这本关于 Python的书。也许从我的亲身故事中，您更能感受到Python可能给您带来的作用，或者对您人生可能的影响。

臣本布衣，躬耕于南充，而非南阳。初中时的政治课本告诉我，没有生产资料的就属于被剥削阶级。而我，唯一的生产资料就是我的头脑，当然，后来就了我的电脑。因此，装有Python的电脑，就算我少得可怜的生产资料了。这可能是我们这些非生而贵，但是对世界充满梦想的有志青年唯一改变命运的工具。Python带给我的，我期望毫无保留地分享给您们，让您们也能够得到Python所有的好。知识与其它所有的东西都不相同，分享知识，只能让我们的知识更有价值。而媳妇和车子是绝对不能分享的。对于我来说，Python的好表现在许多方面。

 Python的好在她给了我论文。我在美国和中国的大学当教授。大家也许知道，对于科研人员，“To publish or to perish”。我们要么发表论文而洛阳纸贵，要么穷得“世界如此之大，却没有安放小小书桌的地方”。我使用Python爬取网页，做大数据研究，分析我的驾驶研究数据，绘制论文的图表。

 Python的好在于代码中自有颜如玉。其实，程序员是一种很浪漫的生物，他们表现出来的Nerd（无趣），只是他们更有责任感。 我们会用Python绘制很浪漫的心或者玫瑰，去向我们心中的女神表白。 

 Python的好在于代码中自有千钟粟。Python给了我不多不少的财富，让我可以给我喜欢的女孩买包包。美国大学的博士生和教授都是一年只有九个月工资。 在没有工资的暑假，我给University of Illinois大学商学院的教授写Python代码，大约30行代码换来了5000美元。

 Python对我的好，馈赠给我的生活， 我都想毫无保留的分享给您们。期望我在书中的分享可以为您们的人生探索提供多一种工具。

 本书以作者超过十年的Python经验，整理了我们在作为程序员，科研人员，教学等的很多案例。本书还涉及了Python在当前许多热点技术话题，例如，爬虫，大数据，认知神经科学和社会网络等。通过学习本书，运行书中的案例代码，并自己迁移式学习做一些案例项目，相信您们也可以成为代码英雄，写得了网页，做得了图表，发表得了论文，玩得转大数据。

 “为什么我需要学习Python？” 如果您想成为未来的Bill Gates， Mark Zuckberg，如果您想实现发表论文，拿到博士学位，上市敲钟，赢娶白富美（或者高富帅），走向人生高峰等等梦想的话，那么，请从在我们的电脑上安装 Python 开始吧。

## 安装配置Python开发环境

## Python 2.X 与3.X
如果您使用的是mac 或者Linux, Unix电脑，那么，恭喜您。您的电脑里一直有Python这个宝藏，只是我们还没有去挖掘它。 对于Windows 用户，您需要去www.python.org下载Python 2.7。建议您下载 Python 2.X的版本，而不是Python 3.X的版本。因为，本书的代码是基于Python 2.X开发和测试的。 另外，有一些Python库等还没有支持Python 3.X的版本。Python的美，除了Python官方安装软件和内置的功能外，还在于Python有数千个库，而且这些库大多数都是由爱好者或者志愿者免费维护的。 我们本着分享精神和与人为善的精神，会努力维护我们的Python库，努力为后来者提供技术支持。 不过，除了Python，在现实生活中， 我们还需要一份付工资的工作，取悦我们的伴侣，养育孩子，孝敬父母，享受我们自己的生活。 因此，虽然Python官方已经发布了Python 3.X版本，但是许多的Python库支持最好的还是Python 2.X。为了避免依赖库缺失的困难，我们强烈建议目前大家使用Python 2.X。

Python语言的官方网址是www.python.org。您可以在www.python.org下载到各个版本针对不同操作系统的Python安装包。为了您的方便，您也可以在www.usee.tech/Downloads/python2.7.msi下载到Python 2.7针对Windows操作系统的安装包。

在安装Python时，除了Python 2.X和 Python 3.X以外，我们还需要注意电脑处理器32位和64位的区别。最近几年买的电脑，基本上都是64位的电脑。如果您在使用一台古老的电脑学习本书， 它可能是32位的电脑。 64位的电脑比32位的电脑可以同时处理更大的内存。 32位的电脑最多同时处理4G的数据。64位处理器的电脑可以运行32位电脑的代码或者Python库，而32位电脑不一定能够运行针对64位电脑的Python代码。所以，为了保证代码对不同电脑的兼容性，您最好安装32位的Python安装包和库。

让新手一入手就来理解不同版本的区别和选择不同的安装包，可能会吓到新手。 请大家别担心，Python很简单。 本书作者们很热情， Python社区也很热情。 在照顾好伴侣和孩子后，我们会第一时间为大家解答Python问题的。 如果遇到安装问题，最快的解决办法就是，尝试下载多上不同版本的Python，分别安装，总有一款适合您。

## 检测Python是否安装成功
检验Python是否安装成功，我们只需要运行Python自带的解释器(Interpreter)就可以了。 解释器是一个可以交互式快速运行简短Python代码的工具。

在Windows操作系统下面， 如果您在安装时不有修改安装目录，Python的解释器应该在C:\python27\python.exe。您只需要双击python.exe就可以运行Windows下的Python解释器了。

在mac操作系统下面，点击右上角的搜索按钮，输入terminal（终端），然后回车，就可以运行terminal了，如图1.1所示。如果您的mac的系统语言是中文，您可能需要输入终端来运行terminal。在terminal中，输入"python"并回车，就可以启动Python的编辑器了。图1.2是mac下运行Python后的界面。

<center><img src="图1.1.terminal for mac.png" width="300"></center>
<center>图1.1. 运行mac操作系统下的terminal（终端）</center>


<center><img src="图1.2.run python under mac.png" width="300"></center>
<center>图1.2. 在mac操作系统下的运行Python交互编程界面</center>

在Unix或者Linux操作系统中，


## 第一个程序，"Hello World"
我们在写所有的语言的第一个程序，基本上都是"Hello World"。Python没有其它语言，比如C和java，复杂的编译过程。Python的"Hello World"可能是所有主流编程语言中最简单的了。我们只需要输入print "Hello World"并回车运行就可以实现"Hello World了"。图1.2显示的就是如何在mac下面实验"Hello World"了。

## 编辑器 (Editor)
相对于解释器的单行交互运行模式，编辑器(Editor)提供了更多的编程附注功能，例如，代码的彩色标识，函数的自动补全等功能。如果我们要写多行代码，建议大家使用编辑器。下面是一些我用过的，或者比较常见的Python编程器。

### Anaconda
Instead of installing Python, and then installing all required external packages separately, you could opt for installing Anaconda. You can download it from the Continuum website: http://store.continuum.io/c- shop/anaconda/. Despite being produced by a company, Anaconda is free. It comes pre-loaded with a lot of cool stuff; but you will still need to download PyGaze, PyGame, PsychoPy, and pyglet.

### Python (X,Y)
Python (X,Y)集成了主要的用于科学技术的Python库，如numpy, scipy, PyQT等。安装Python (X,Y)
后，常用的Python包就基本上有了。 

### Spyder
Spyder是基于PyQt库写的类似Matlab界面的Python编辑器，比较适合喜欢Matlab的读者。

### Pyscripter
Pyscripter是一款比较轻巧的编辑器， 主要适用于Windows操作平台，没有Mac和ubuntu版本。 我在教学中经常用Pyscripter，主要是因为它安装文件小，学生安装配置快。另外一个重要原因是Pyscripter的代码编辑界面和交互界面，都可以通过滚动鼠标滑鼠快速放大字体，可以让上课的同学们可以看清电脑上的字体。

### Visual Studio Code
我在工作中用Visual Studio Code比较多，主要是因为它的跨平台性。我经常在mac或者windows操作系统下交替工作。 所以，我期望得到一个编辑器可以在两个操作系统下都有相似的交互界面。此外， 我期望我使用多种语言时，都可以采用相同的编辑器。 Visual Studio Code支持绝大多数常用编程语言，而且可以通过插件快速定置编辑器功能。

### Eclipse
Eclipse是在微软推出跨平台的Visual Studio Code之前，我用得比较多的编辑器。主要原因也是因为我期望在为不同的语言在mac和Windows下都使用相同的编辑器。在Google 不为Eclipse提供支持来编写Android程序后，我使用Eclipse的频率就下降了。 

## 如何安装 Python库
### 通过setup.py源文件安装 Python库

### 使用.exe打包好的安装库
使用.exe安装打包好的安装库，与我们安装Python编程语言本身一样简单。您需要做的，仅仅是下载合适您电脑类型（32位或者64位）和适合您Python版本（Python 2.X或者3.X）的安装库，然后一路点击下一步就可以完成安装了。 

### 使用pip或者easy_tools等包管理软件安装Python库

本书使用到的 Python 库
TABLE 1.1 Python libraries used in this book

