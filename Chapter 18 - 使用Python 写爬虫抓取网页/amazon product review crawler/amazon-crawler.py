__author__ = 'He'

'''
http://www.runtime-era.com/2011/08/quick-tutorial-parsing-website-in.html
'''

from BeautifulSoup import BeautifulSoup
import urllib

url ='http://www.amazon.com/gp/cdp/member-reviews/A2D1LPEUCTNT8X?ie=UTF8&display=public&page=1&sort_by=MostRecentReview'
pageFile = urllib.urlopen(url)
pageHtml = pageFile.read()
pageFile.close()
soup = BeautifulSoup("".join(pageHtml))

#print soup


def getReviewEffort(soup):
    # get the review effort: time
    #print soup.findAll("span", {"class":"tiny"})
    
    # get reivew text
    
    reviewTexts =  soup.findAll("div", {"class":"reviewText"})
    
    
    print reviewTexts[0]
    
    print "---------------------------review effort -------------------"
    effortText= reviewTexts[0].find("span", {"class":"tiny"})
    print effortText.contents[0]



    # reviewed product.

def getLinks(soup):
    #sample
    # the following will get "<span class="h3color tiny">This review is from: </span>,
    linkspart= soup.findAll("div", {"class":"tiny"})
    for i in range(len(linkspart)):
        links = linkspart[i].find("a")
        print links
        print links['href']
        print


getLinks(soup)