# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 21:22:31 2015


@author: hejibo
how to use pickle

http://blog.csdn.net/xiaofeng_yan/article/details/6657983

for memberID= 'A2D1LPEUCTNT8X' # top 1 reviewer

failed for 166 page
failed for 171 page
failed for 182 page
failed for 183 page
failed for 195 page
failed for 198 page
failed for 199 page
failed for 211 page

"""

import cPickle as p1
from BeautifulSoup import BeautifulSoup
import urllib


#memberID='A1E1LEVQ9VQNK' # top 2 reviewer
memberID= 'A2D1LPEUCTNT8X' # top 1 reviewer
for PageIndex in xrange(157,295+1):
    #PageIndex=1
    try:
        url ='http://www.amazon.com/gp/cdp/member-reviews/%s?ie=UTF8&display=public&page=%d&sort_by=MostRecentReview'%(memberID,PageIndex)
        pageFile = urllib.urlopen(url)
        pageHtml = pageFile.read()
        pageFile.close()
        soup1 = BeautifulSoup("".join(pageHtml))
        reviewfile = 'DataCrawled/%s/amazon-sample-review-%d-page.data'%(memberID,PageIndex)
        # the name of the file where we will store the object
        # Write to the file
    
        f = file(reviewfile, 'w')
        p1.dump(soup1, f) # dump the object to a file
        f.close()
    except:
        print 'failed for %d page'%PageIndex
