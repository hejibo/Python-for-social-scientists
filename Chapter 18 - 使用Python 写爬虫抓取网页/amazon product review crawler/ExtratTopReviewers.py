# -*- coding: utf-8 -*-
"""
Created on Wed Jan 28 22:49:56 2015

@author: DrHe

Bugs:

some users may have non-english characters
UnicodeEncodeError: 'ascii' codec can't encode character u'\u017d' in position 13: ordinal not in range(128)

"""

from BeautifulSoup import BeautifulSoup
import urllib
import cPickle as p




def CrawlPage(PageIndex):
    try:
        url ='http://www.amazon.com/review/top-reviewers/ref=cm_cr_tr_link_2?ie=UTF8&page=%s'%PageIndex
        pageFile = urllib.urlopen(url)
        pageHtml = pageFile.read()
        pageFile.close()
        reviewfile = 'Top Reviewer List/amazon-top-reviewers-%d-page.data'%PageIndex
        # the name of the file where we will store the object
        # Write to the file
        soup = BeautifulSoup("".join(pageHtml))
    
        f = file(reviewfile, 'w')
        p.dump(soup, f) # dump the object to a file
        f.close()
    except:
        print 'failed for %d page'%PageIndex

def LoadCachedPage(PageIndex):
    reviewfile = 'Top Reviewer List/amazon-top-reviewers-%d-page.data'%PageIndex
    f = file(reviewfile)
    soup = p.load(f)
    f.close()
    return soup



def getNames(soup,PageIndex):
    '''
    get text between links
    http://stackoverflow.com/questions/6251319/extract-text-between-link-tags-in-python-using-beautifulsoup
    '''
    dataSetLinks=[]
    #sample
    # the following will get "<span class="h3color tiny">This review is from: </span>,
    soupParsed = BeautifulSoup(soup)
    print soupParsed
    reviewIndexStart = 1+(PageIndex-1)*10
    reviewIndexEnd =11+(PageIndex-1)*10
    for reviewIndex in range(reviewIndexStart,reviewIndexEnd):
        #reviewIndex=1
        print "-------------------------------------------------------"
        print reviewIndex
        datapart= soupParsed.find("tr", {"id":"reviewer%s"%reviewIndex})
        
        hyperlinks=datapart.findAll("a")
        reviewerID= hyperlinks[1]['name']
        
        tableValues = datapart.findAll("td", {"class":"crNum"})
        
        
        rankIndexValue=tableValues[0].text
        rankIndexValue=rankIndexValue[rankIndexValue.find("#")+1:]
        TotalReviews =tableValues[1].text	
        HelpfulVotes = tableValues[2].text
        
        
        crNumPercentHelpful = datapart.find("td", {"class":"crNumPercentHelpful"}).text
        crNumFanVoters = datapart.find("td", {"class":"crNumFanVoters"}).text
        print rankIndexValue
        print TotalReviews
        print HelpfulVotes
        print crNumPercentHelpful
        print crNumFanVoters
        textInTable = datapart.text
        print textInTable
        name = textInTable[textInTable.find(rankIndexValue)+len(rankIndexValue):textInTable.find("See all")]
        print "\nname:",name
        dataSetLinks.append([rankIndexValue,name,reviewerID,TotalReviews,HelpfulVotes,crNumPercentHelpful,crNumFanVoters])

    return dataSetLinks

dataSetLinksAllPage=[]
for PageIndex in range(1,1001):
    print '--------------------------------------------------------'
    print 'process page:',PageIndex
    #PageIndex=2
    #CrawlPage(PageIndex)
    try:
        soup = LoadCachedPage(PageIndex)
        #print soup
        #getReviewerRank(soup)
        dataSetLinks = getNames(soup,PageIndex)
        dataSetLinksAllPage.extend(dataSetLinks)
    except:
        'failed processing page'
    #break

for (rankIndexValue,name,reviewerID,TotalReviews,HelpfulVotes,crNumPercentHelpful,crNumFanVoters) in dataSetLinksAllPage:
    print [rankIndexValue,name,reviewerID,TotalReviews,HelpfulVotes,crNumPercentHelpful,crNumFanVoters]

def WriteDataCSV(outputArray):
    outfile = open('amazon-reviewer-list-complete.csv','w')
    rowIndex=0
    print >>outfile,'rankIndexValue','\t','name','\t','reviewerID','\t','TotalReviews','\t','HelpfulVotes','\t','crNumPercentHelpful','\t','crNumFanVoters'
    for (rankIndexValue,name,reviewerID,TotalReviews,HelpfulVotes,crNumPercentHelpful,crNumFanVoters) in outputArray:
        try:        
            print >>outfile,rankIndexValue,'\t',name,'\t',reviewerID,'\t',TotalReviews,'\t',HelpfulVotes,'\t',crNumPercentHelpful,'\t',crNumFanVoters
        except:
            print rankIndexValue,'\t',name,'\t',TotalReviews,'\t',HelpfulVotes,'\t',crNumPercentHelpful,'\t',crNumFanVoters

    outfile.close()
    

WriteDataCSV(dataSetLinksAllPage)
print 'haha-- write finished'