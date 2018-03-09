__author__ = 'He'

'''
http://www.runtime-era.com/2011/08/quick-tutorial-parsing-website-in.html

how to use pickle

http://blog.csdn.net/xiaofeng_yan/article/details/6657983
'''
# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
import urllib
import cPickle as p

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
#print soup

#print soup


def getReviewEffort(soup):
    dataSet =[]
    # get the review effort: time
    #print soup.findAll("span", {"class":"tiny"})
    
    # get reivew text
    
    reviewTexts =  soup.findAll("div", {"class":"reviewText"})
    
    
    for i in range(len(reviewTexts)):
        reviewTextsRaw= reviewTexts[i].text
        #reviewTextsRaw contains javascript. 
        
        #use "Length:: 0:22 Mins" as anchor to remove the javascript. 
        reviewTextsClean = reviewTextsRaw[reviewTextsRaw.find('Mins')+4:]
        #print reviewTextsClean
        
        #print "---------------------------review effort -------------------"
        effortText= reviewTexts[i].find("span", {"class":"tiny"})
        effortValue = effortText.contents[0]
        #print effortValue
        dataSet.append((reviewTextsClean,effortValue))
    #print dataSet
    return dataSet
    



    # reviewed product.

def getLinks(soup):
    '''
    get text between links
    http://stackoverflow.com/questions/6251319/extract-text-between-link-tags-in-python-using-beautifulsoup
    '''
    dataSetLinks=[]
    #sample
    # the following will get "<span class="h3color tiny">This review is from: </span>,
    linkspart= soup.findAll("div", {"class":"tiny"})
    for i in range(len(linkspart)):
        #print '--------------------------------------'
        links = linkspart[i].find("a")
        #print links
        #print
        if links:#when links is not None
            linkUrl= links['href']
            linkText = links.text
            #print linkUrl
            #print linkText
            dataSetLinks.append((linkUrl,linkText))
        print
    return dataSetLinks

def GetStarRating(soup):
    
    '''
    http://stackoverflow.com/questions/20649048/display-text-from-img-alt-tag-with-beautifulsoup
    
    <span style="margin-left: -5px;"><img src="http://g-ecx.images-amazon.com/images/G/01/x-locale/common/customer-reviews/stars-5-0._V192240867_.gif" width="64" alt="5.0 out of 5 stars" title="5.0 out of 5 stars" height="12" border="0" /> </span>
    '''
    StarSet =[]
    stars =  soup.findAll("span", {"style":"margin-left: -5px;"})
    for i in range(len(stars)):
        starsImage =  stars[i].find("img")
        #print stars[0]
        starRating =  starsImage['alt']
        #print 
        StarSet.append(starRating)
    return StarSet
    
#dataSetLinks = getLinks(soup)
#dataset = getReviewEffort(soup)
    
StarSet = GetStarRating(soup)
for star in StarSet:
    print star
#for (reviewTextsClean,effortValue) in dataset:
#    print (reviewTextsClean,effortValue)
#    print '--------------------------------'

#for (linkUrl,linkText ) in dataSetLinks[1:]:
#    # the first link set is 
#    #http://www.amazon.com/review/top-reviewers 1
#    # which is not links to products, thus links to be excluded. 
#    print linkUrl,linkText
#    print '--------------------------------'
#    
#print len(dataSetLinks),len(dataset)
#
#outputArray=zip(dataSetLinks[1:],dataset)
#for ((reviewTextsClean,effortValue),(linkUrl,linkText )) in outputArray:
#    print reviewTextsClean,effortValue,linkUrl,linkText
#    print '--------------------------------'


    
def WriteDataCSV(outputArray):
    outfile = open('amazon-review-sample.csv','w')
    rowIndex=0
    print >>outfile,'reviewTextsClean','\t','effortValue','\t','linkUrl','\t','linkText'
    for ((reviewTextsClean,effortValue),(linkUrl,linkText )) in outputArray:
        print >>outfile,reviewTextsClean,'\t',effortValue,'\t',linkUrl,'\t',linkText

    outfile.close()
    

#WriteDataCSV(outputArray)