# -*- coding: utf-8 -*-
"""
Created on Sun May 17 22:28:23 2015

@author: Jibo

Crawl number of review pages


http://www.amazon.com/gp/cdp/member-reviews/A2D1LPEUCTNT8X?ie=UTF8&display=public&page=1&sort_by=MostRecentReview


sample reviewer #:
    A2D1LPEUCTNT8X
    A1E1LEVQ9VQNK

    http://www.amazon.com/gp/cdp/member-reviews/A1E1LEVQ9VQNK?ie=UTF8&display=public&page=1&sort_by=MostRecentReview

"""


import cPickle as p1
import urllib

def CrawlPage(PageIndex):
    try:
        url ='http://www.amazon.com/gp/cdp/member-reviews/A3TWBW1B17R151?ie=UTF8&display=public&page=%s&sort_by=MostRecentReview'%PageIndex
        pageFile = urllib.urlopen(url)
        pageHtml = pageFile.read()
        pageFile.close()
        reviewfile =r'D:\OneDrive\Research\amazon online review\Step 3. crawl number of review pages\Reviewer First Page Cache\amazon-product-review-%d-page.data'%PageIndex
        # the name of the file where we will store the object
        # Write to the file

        f = file(reviewfile, 'w')
        p1.dump(pageHtml, f) # dump the object to a file
        f.close()
        print 'finished page:'%PageIndex
    except:
        print '!!!!!!!!!!!!!!!!!!!!!!!!failed for %d page'%PageIndex
#
#for PageIndex in xrange(1,1000):
#    #PageIndex=1
#    CrawlPage(PageIndex)

def CrawlPageTest(PageIndex,reviewerID):

    url ='http://www.amazon.com/gp/cdp/member-reviews/%s?ie=UTF8&display=public&page=%s&sort_by=MostRecentReview'%("A2KBF2OYR359AJ",9)
    print url
    pageFile = urllib.urlopen(url)
    pageHtml = pageFile.read()
    pageFile.close()
    reviewfile = r"/Users/hejibo/OneDrive/Research/amazon online review/Step 4. crawl  all review pages 2/All review page cache/A2KBF2OYR359AJ/reviewer-A2KBF2OYR359AJ-9-page.data"
    # the name of the file where we will store the object
    # Write to the file

    f = file(reviewfile, 'w')
    p1.dump(pageHtml, f) # dump the object to a file
    f.close()

def ReadReviewerIDFile():
    filename = "amazon-reviewer-list-complete-id-only.csv"
    infile = open(filename,'r')
    reviewIDList =[ reviewID.strip() for reviewID in infile.readlines()]
    infile.close()
    return reviewIDList



reviewIDList= ReadReviewerIDFile()
print reviewIDList

for reviewerID in reviewIDList:
    reviewerID = 'A2D1LPEUCTNT8X'
    PageIndex = 0
    print reviewerID
    CrawlPageTest(PageIndex,reviewerID)
    break

print "-_-!!"