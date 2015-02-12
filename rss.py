import requests
import rss_parser
from bs4 import BeautifulSoup

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
            'From' : 'isayhellotoyou@gmail.com'
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
            