# 第1章 - Python 的变量

作者： 何吉波博士，优视眼动科技公司创始人，hejibo@usee.tech, [http://www.usee.tech](http://www.usee.tech)  

Python语言的变量主要用于存储数据。变量的类型有许多重，包括数字 (Numbers)、字符串 (Strings)、逻辑变量 (Booleans)、集合 (Sets)、列表 (Lists)、元组 (Tuples)、数组 (NumPy arrays)和字典 (Dictionary)等。下面我们将分别介绍这些变量类型。

## 变量名
 Python的变量名可以是以英文字符或者下划线(_)开始的任何变量，如_hello, This, thisVariable等。大家需要注意的是， Python的变量名是大小写敏感的。This和this是不同的变量。 此外， Python的变量名不能是语言内置的保留字。下面的表格显示的是Python的保留字的列表。
 
## 赋值
与Java或者C语言等不同， Python的变量并不需要提前申明，可以直接赋值。Python的一个变量名也可以重新赋予一个新的类型的变量值，而通常不需要强制地进行数据类型的转换。
比如下面的代码，可以直接将一个字符串“Hello World”和浮点数1.0直接赋给thisString这个变量名。

```python
thisString = "Hello World"
thisString = 1.0

```

Python的变量不需要提前申明，赋予新值时也不需要强制转换，可以让Python的代码更加简洁。但缺乏申明等也会让代码容易出现Bug。我们的Python代码出错时，经常是由于变量名的大小写没有注意， 或者是后面的一个变量名与代码前部分的变量名重复，导致了变量被覆盖了。

## 数字 (Numbers)
Python的数字变量主要包括整型(Integer)和浮点型（Float）两类。整型数字就是不带小数部分的变量， 比如520，0，-52。浮点数字是带小数部分的变量，如0.0， 3.1415926和520025.1314等。整型和浮点型可以相互转换。int(520025.1314)的输出结果为整型520025。float(0)的输出结果为浮点数0.0。

## 字符串 (Strings)

## 逻辑变量 (Booleans)

## 集合 (Sets)

## 列表 (Lists)

## 元组 (Tuples)

## 数组 (NumPy arrays)

## 字典 (Dictionary)
