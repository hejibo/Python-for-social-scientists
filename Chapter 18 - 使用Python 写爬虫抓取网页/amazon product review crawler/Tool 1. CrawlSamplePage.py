__author__ = 'hejibo'
'''
crawl a sample webpage
'''

import multiprocessing as mp
import random
import string
import threading
from time import ctime,sleep

import urllib
from BeautifulSoup import BeautifulSoup
import urllib2
import cPickle as p

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

def ensure_dir(path):
    '''ensure a directy is valid for creating a file, if the directory does not exist,
    create the directory'''
    import os
    d = os.path.dirname(path)
    if not os.path.exists(d):
        os.makedirs(d)


def LoadCachedPage(reviewfile):

    #reviewfile = r"/Users/hejibo/Downloads/Step 4. crawl  all review pages/All review page cache/%s/reviewer-%s-%s-page.data"%(reviewerID,reviewerID,PageIndex)
    # the name of the file where we will store the object
    # Write to the file

    f = file(reviewfile)
    soup = p.load(f)
    f.close()
    return soup

def CrawlPageTest(url):

    #url ='http://www.amazon.com/gp/cdp/member-reviews/%s?ie=UTF8&display=public&page=%s&sort_by=MostRecentReview'%(reviewerID,PageIndex)
    pageFile = urllib2.urlopen(url,timeout=5)
    pageHtml = pageFile.read()
    pageFile.close()
    ensure_dir('/Users/hejibo/Downloads/Step 4. crawl  all review pages/sample pages/')
    reviewfile =r'/Users/hejibo/Downloads/Step 4. crawl  all review pages/sample pages/testurl.data'
    # the name of the file where we will store the object
    # Write to the file

    f = file(reviewfile, 'w')
    p.dump(pageHtml, f) # dump the object to a file
    f.close()
    #break

            #continue
url = 'http://www.amazon.com/gp/cdp/member-reviews/A3TWBW1B17R151?ie=UTF8&display=public&page=%s&sort_by=MostRecentReview'

CrawlPageTest(url)
print '-_-!'

reviewfile =r'/Users/hejibo/Downloads/Step 4. crawl  all review pages/sample pages/testurl.data'
soup = LoadCachedPage(reviewfile)
print soup

