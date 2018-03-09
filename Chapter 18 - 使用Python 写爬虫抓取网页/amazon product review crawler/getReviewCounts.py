# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 22:13:31 2015

@author: hejibo
get total review number and total page number
"""
from BeautifulSoup import BeautifulSoup
import urllib
import cPickle as p
import re

#url ='http://www.amazon.com/gp/cdp/member-reviews/A2D1LPEUCTNT8X?ie=UTF8&display=public&page=1&sort_by=MostRecentReview'
#pageFile = urllib.urlopen(url)
#pageHtml = pageFile.read()
#pageFile.close()
#soup = BeautifulSoup("".join(pageHtml))

# Read back from the storage
reviewfile = 'amazon-sample-review.data'
f = file(reviewfile)
soup = p.load(f)
f.close()

def ReviewCounts(soup):
    reviewCounts =  soup.findAll("div", {"class":"small"})
    reviewCountsLabels = reviewCounts[0].text
    
    #m = re.match(r'[0-9]', str(reviewCountsLabels))
    
    totalReview = int(re.findall(r'\d+', reviewCountsLabels)[0])
    print totalReview
    if mod(totalReview,10)==0:
        totalPageCount = int(totalReview/10)
    else: 
        totalPageCount = int(totalReview/10)+1
    print totalPageCount
    return totalReview,totalPageCount
    
totalReview,totalPageCount = ReviewCounts(soup)
print totalReview,totalPageCount
