import wx
import wx.lib.stattext as ST
from wx.lib.wordwrap import wordwrap
import wx.lib.scrolledpanel as scrolled
import requests
from urlparse import urlparse
import rss
import wx.lib.agw.ultimatelistctrl as ULC
import wx.html2

class Application(wx.Frame):
    
    def __init__(self, parent, title, *args, **kwargs):
        super(Application, self).__init__(parent, title='OGLE', size=(1300,800))
        
        self.InitUI()
        self.Centre()
        self.Show()
    
    def InitUI(self):
        
        self.panel = wx.Panel(self)
        self.feed_page_list = {}
        self.current = None
        
        top_layer_vbox = wx.BoxSizer(wx.VERTICAL)
        
        gridbox = wx.GridSizer(5,5,5,5)
        keyword_button = wx.Button(self.panel, label='TAG')
        gridbox.Add(keyword_button)
        
        button = wx.Button(self.panel, label='ADD')

        result = button.Bind(wx.EVT_LEFT_DOWN, self.add_url)
        
        
        #hbox1.Add(wx.StaticText(self.panel, label='Top Box', size=(1300,100)), proportion=1, flag=wx.EXPAND)
        gridbox.Add(button)
        top_layer_vbox.Add(gridbox, flag=wx.EXPAND)
        
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        top_layer_vbox.Add(self.hbox2, flag=wx.EXPAND, proportion=1)
        
        
        self.listbox = wx.ListBox(self.panel, size=(180,1))
        self.listbox.Bind(wx.EVT_LISTBOX, self.display)
        
        ###testing purposes
        #self.listbox.Append('http://lifehacker.com')
        
        vbox1 = wx.BoxSizer(wx.VERTICAL)   
        vbox1.Add(self.listbox, proportion=1, flag=wx.EXPAND)
        
        self.hbox2.Add(vbox1, flag=wx.EXPAND)
        
        #scrolled_panel = scrolled.ScrolledPanel(self.panel)
        
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        

        self.mult_listbox = MultilineListBox(self.panel, self.feed_page_list)
        """for i in range(5):
                                    st = ArticleBox(scrolled_panel, description='Article #' + str(i))
                                    vbox2.Add(st.get_description(), proportion=1, flag=wx.EXPAND | wx.BOTTOM, border=5)
                                """
        vbox2.Add(self.mult_listbox, proportion=1, flag=wx.EXPAND)
        self.mult_listbox.Bind(wx.EVT_LISTBOX, self.update_browser)
        
        self.hbox2.Add(vbox2, flag=wx.EXPAND)
        #self.panel.SetSizer(vbox2)
        
        #vbox3 = wx.BoxSizer(wx.VERTICAL)
        self.simple_browser = wx.html2.WebView.New(self.panel)

        #st = wx.StaticText(self.panel, label='Hello World!')
        #st.Wrap(1000)
        #vbox3.Add(simple_browser, proportion=1, flag=wx.EXPAND)
        self.hbox2.Add(self.simple_browser, proportion=1, flag=wx.EXPAND)
        
        #scrolled_panel.SetAutoLayout(1)
        #scrolled_panel.SetupScrolling(scroll_x=False)
        #scrolled_self.panel.ShowScrollbars(wx.SHOW_SB_NEVER,wx.SHOW_SB_NEVER)
        
        
        self.panel.SetSizer(top_layer_vbox)

        
    def add_url(self, event):
        entry = wx.TextEntryDialog(self.panel, 'Add URL: ', '')
        entry.ShowModal()
        url = entry.GetValue()
        #parsed = urlparse(result)
        # all cased url inputs
        """if not bool(parsed.scheme):
            parsed._replace(**{'scheme' : 'http'})
            parsed = urlparse(parsed.geturl())"""
        first_working_link = rss.FeedPage(url).feed
        if first_working_link:
            self.listbox.Append(url)
            self.feed_page_list[url] = first_working_link
        
    def display(self, event):
        url = self.listbox.GetString(self.listbox.GetSelection())
        self.current = url
        #self.feed_page = rss.FeedPage(url)
        #combine clear_links & Clear!
        self.mult_listbox.clear_links()
        self.mult_listbox.Clear()
        self.mult_listbox.update(self.feed_page_list[url])
        self.mult_listbox.Refresh()
        """for i in range(5):
            st = ArticleBox(scrolled_panel, description='Article #' + str(i))
            vbox2.Add(st.get_description(), proportion=1, flag=wx.EXPAND | wx.BOTTOM, border=5)
        """

    def update_browser(self, event):
        num = self.mult_listbox.GetSelection()

        if self.current:
            self.simple_browser.LoadURL(self.mult_listbox.links[num])
        #Need exception raised

class MultilineListBox(wx.HtmlListBox):
    def __init__(self, parent, feed):
        wx.HtmlListBox.__init__(self, parent, size=(400,200))
        #NO assume 0 setitemcount!
        self.SetItemCount(20)
        self.data = feed
        self.links = []

    def OnGetItem(self, n):
        feed = self.data.entries
        txt = ''
        for text in rss.BeautifulSoup(feed[n].description).stripped_strings:
            txt += text
            self.links.append(feed[n].link)
        return '%s\n' % txt[:150]
        
    def update(self, feed):
           self.data = feed

           #len needed fixed
           self.SetItemCount(20)
           self.Refresh()
           
    def clear_links(self):
        self.links = []

"""class SimplrBrowser(wx.Dialog):
    def __init__(self, *args, **kwargs):
        wx.Dialog.__init__(self, *args, **kwargs)
        self.browser = wx.html2.WebView.New(self)"""


#might be removed
class ArticleBox():
    def __init__(self, parent, description='', url=''):
        parsed_description = wordwrap(description, 300, wx.ClientDC(parent))
        self.static_text = ST.GenStaticText(parent, -1, parsed_description, size=(300,300))
        self.url = url
    
    def get_description(self):
        return self.static_text
        
    def get_url(self):
        return self.url
    
if __name__ == '__main__':
    app = wx.App()
    Application(None, title='rss needs name!')
    app.MainLoop()