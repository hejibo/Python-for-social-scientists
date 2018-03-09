# -*- coding: utf-8 -*-
"""
Created on Wed Jan 28 22:00:16 2015

@author: DrHe

"""

import cPickle as p1
import urllib

def CrawlPage(PageIndex):
    try:
        url ='http://www.amazon.com/review/top-reviewers/ref=cm_cr_tr_link_2?ie=UTF8&page=%s'%PageIndex
        pageFile = urllib.urlopen(url)
        pageHtml = pageFile.read()
        pageFile.close()
        reviewfile = 'Top Reviewer List/amazon-top-reviewers-%d-page.data'%PageIndex
        # the name of the file where we will store the object
        # Write to the file
    
        f = file(reviewfile, 'w')
        p1.dump(pageHtml, f) # dump the object to a file
        f.close()
    except:
        print 'failed for %d page'%PageIndex
#
#for PageIndex in xrange(1,1000):
#    #PageIndex=1
#    CrawlPage(PageIndex)

def CrawlPageTest(PageIndex):

    url ='http://www.amazon.com/review/top-reviewers/ref=cm_cr_tr_link_2?ie=UTF8&page=%s'%PageIndex
    pageFile = urllib.urlopen(url)
    pageHtml = pageFile.read()
    pageFile.close()
    reviewfile = 'Top Reviewer List/amazon-top-reviewers-%d-page.data'%PageIndex
    # the name of the file where we will store the object
    # Write to the file

    f = file(reviewfile, 'w')
    p1.dump(pageHtml, f) # dump the object to a file
    f.close()

for PageIndex in [100,103,108,109,11,110,116,228,237,249,378,381,418,452,48,50,530,532,57,705,711,75,767,777,78,809,83,830,831,89,909,913,951,969,99]:
    CrawlPageTest(PageIndex)
