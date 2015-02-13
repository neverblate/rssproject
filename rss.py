import requests
import rss_parser
import urllib2
from urlparse import urlparse
import feedparser
from bs4 import BeautifulSoup

FEED_LINKS_ATTRIBUTES = {
    (('type', 'application/rss+xml'),),
    (('type', 'application/atom+xml'),),
    (('type', 'application/rss'),),
    (('type', 'application/atom'),),
    (('type', 'application/rdf+xml'),),
    (('type', 'application/rdf'),),
    (('type', 'text/rss+xml'),),
    (('type', 'text/atom+xml'),),
    (('type', 'text/rss'),),
    (('type', 'text/atom'),),
    (('type', 'text/rdf+xml'),),
    (('type', 'text/rdf'),),
    (('rel', 'alternate'), ('type', 'text/xml')),
    (('rel', 'alternate'), ('type', 'application/xml'))
}

class RssPage():
    def __init__(self, url):
        """
        Initialize a RssPage instance
        
        url: home url
        source: BeautifulSoup object
        item_list: all <item> in a rss page
        """
        self.url = url
        self.source = None
        self.item_list = []
        self.title_list = []
        self.desc_list = []
        
        params = {
            'User-Agent' : 'Mozilla/5.0',
            'Host' : 'miteshshama.com',
            'From' : 'miteshshama@gmail.com'
        }
        
        print 'self.url', self.url
        r = requests.get(self.url)
        print 'r.url', r.url
        soup = BeautifulSoup(r.content)
        print soup.prettify()
        # is there other better ways?
        rss_link = soup.find_all(attrs={'type' : 'application/rss+xml'})
        print 'find all', rss_link
        if rss_link:
            # need generalized
            temp_link = rss_link[0]['href']
            if ('http' not in temp_link):
                temp_link = self.url + temp_link
            print 'templink', temp_link
            r_rss = requests.get(temp_link)
            self.source = BeautifulSoup(r_rss.content)
            self.item_list = self.source.find_all('item')
            
            # ordered list - <title> <desc>
            for item in self.item_list:
                self.title_list.append(self._parser(item.title.text))
                self.desc_list.append(self._parser(item.description.text))
            
        else:
            raise Exception("RSS link(s) not found!")
    
    def get_title(self, part='item'):
        """
        Returns a page title or a list of article titles
        
        from: title of a rss page or of all articles
                either string 'item' or 'channel'
        """
        if (part == 'item'):
            return self.title_list
        elif (part == 'channel'):
            # implement later
            return None
        else:
            raise Exception('Argument out of scope')
    
    def get_description(self):
        """
        Return a list of description tags' contents 
        of each article
        """
        return self.desc_list
        
    def _parser(self, html):
        """
        Parse html tags, and returns only text
        Gets called automatically
        
        html: HTML content
        """
        html_parser = rss_parser.RssParser()
        html_parser.feed(html)
        return html_parser.get_data()
            
class FeedPage():
    def __init__(self, url):
        self.working_feed_links_list = self._get_working_feed_links_list(url)
        # assume first link!
        self.feed = feedparser.parse(self.working_feed_links_list[0])
                       
    def _extract_feed_links(self, html, feed_links_attributes=FEED_LINKS_ATTRIBUTES):
        """
        Returns generator yielding feed links of a HTML page
        """
        soup = BeautifulSoup(html)
        head_tags_list = soup.find_all('head')
        links_list = []
        for attrs in feed_links_attributes:
            for head in head_tags_list:
                for link in head.find_all('link', dict(attrs)):
                    href = dict(link.attrs).get('href', '')
                    # filter comments feed
                    if href:
                        yield unicode(href)
                    
    def _get_working_feed_links_list(self, url):
        """
        Returns a list of all working feed links url
        """
        # if the url is a feed itself, returns it
        content = urllib2.urlopen(url).read(1000000)
        feed = feedparser.parse(content)
    
        if not feed.get('bozo', 1):
            return unicode(url)
    
        # construct the site url
        parsed_url = urlparse(url)
        site_url = u'%s://%s' % (parsed_url.scheme, parsed_url.netloc)
    
        working_feed_links_lists = []
        for link in self._extract_feed_links(content):
            if '://' not in link:
                link  = site_url + link
            feed = feedparser.parse(link)

            if not feed.get('bozo', 1):
                working_feed_links_lists.append(link)
        return working_feed_links_lists
    
    
if __name__ == "__main__": 
    URL = ['http://techcrunch.com', 
    'http://www.digg.com/', 
    'http://www.engadget.com/',
    'http://www.fastcompany.com/',
    'http://gigaom.com/',
    'http://mashable.com/',
    'http://thenextweb.com/',
    'http://www.lifehacker.com/',
    'http://venturebeat.com/',
    'http://www.theverge.com/',
    'http://www.wired.com/'] 
    for url in URL:
        try:
            print '======== Results from %s ========' % url
            feed_page = FeedPage(url)
            print feed_page.feed.version
            #print feed_page._working_feed_links_list
            print 'Title: ', feed_page.feed.entries[0].title
            try:
                print 'Author: ', feed_page.feed.entries[0].author
            except:
                pass
            print 'Link: ', feed_page.feed.entries[0].link
            print 'Published: ', feed_page.feed.entries[0].published
            print 'Updated: ', feed_page.feed.entries[0].updated
            print 'Description: ', feed_page.feed.entries[0].description
            print '\n'
        except:
            pass
    print '======== END ======='