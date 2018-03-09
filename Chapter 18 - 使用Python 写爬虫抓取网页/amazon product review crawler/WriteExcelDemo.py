# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 21:51:09 2015

@author: hejibo
"""

import xlwt
wbk =xlwt.Workbook()
sheet =wbk.add_sheet('sheet 1')
#Now that the sheet is created, it’s very easy to write data to it.

# indexing is zero based, row then column
sheet.write(0,1,'test text')
#When you’re done, save the workbook (you don’t have to close it like you do with a file object)

wbk.save('test.xls')


def WriteDataExecel(outputArray):
    import xlwt
    wbk =xlwt.Workbook(encoding="utf-8")
    sheet =wbk.add_sheet('sheet 1')
    #Now that the sheet is created, it’s very easy to write data to it.
    rowIndex=0
    for ((reviewTextsClean,effortValue),(linkUrl,linkText )) in outputArray:
        print reviewTextsClean,effortValue,linkUrl,linkText
        # indexing is zero based, row then column
        sheet.write(rowIndex,1,reviewTextsClean)
        sheet.write(rowIndex,2,effortValue)
        sheet.write(rowIndex,3,linkUrl)
        sheet.write(rowIndex,4,linkText)
        rowIndex=rowIndex+1
        break
    #When you’re done, save the workbook (you don’t have to close it like you do with a file object)
    
    wbk.save('amazon-review-sample.xls')
    
#WriteDataExecel(outputArray)