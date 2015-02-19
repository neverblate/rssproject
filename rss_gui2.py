#http://youtu.be/TJfrNo3Z-DU

import wx
import wx.lib.stattext as ST
from wx.lib.wordwrap import wordwrap
import wx.lib.scrolledpanel as scrolled
import requests
from urlparse import urlparse
import rss
import wx.lib.agw.ultimatelistctrl as ULC

class Application(wx.Frame):
    
    def __init__(self, parent, title, *args, **kwargs):
        super(Application, self).__init__(parent, title='What is my name, anyway?', size=(1300,800))
        
        self.InitUI()
        self.Centre()
        self.Show()
    
    def InitUI(self):
        
        self.panel = wx.Panel(self)
        self.feed_page = None
        
        top_layer_vbox = wx.BoxSizer(wx.VERTICAL)
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        
        button = wx.Button(self.panel, label='ADD')

        result = button.Bind(wx.EVT_LEFT_DOWN, self.add_url)
        
        
        #hbox1.Add(wx.StaticText(self.panel, label='Top Box', size=(1300,100)), proportion=1, flag=wx.EXPAND)
        hbox1.Add(button)
        top_layer_vbox.Add(hbox1, flag=wx.EXPAND)
        
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        top_layer_vbox.Add(self.hbox2, flag=wx.EXPAND, proportion=1)
        
        
        self.listbox = wx.ListBox(self.panel)
        self.listbox.Bind(wx.EVT_LISTBOX, self.display)
        
        ###testing purposes
        self.listbox.Append('http://lifehacker.com')
        
        vbox1 = wx.BoxSizer(wx.VERTICAL)   
        vbox1.Add(self.listbox, proportion=1, flag=wx.EXPAND)
        
        self.hbox2.Add(vbox1, flag=wx.EXPAND)
        
        scrolled_panel = scrolled.ScrolledPanel(self.panel)
        
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        # temp implt
        r = requests.get('http://lifehacker.com')
        content = r.content
        for i in range(5):
            st = ArticleBox(scrolled_panel, description='Article #' + str(i))
            vbox2.Add(st.get_description(), proportion=1, flag=wx.EXPAND | wx.BOTTOM, border=5)
        
        list = ULC.UltimateListCtrl(self, wx.ID_ANY)
        
        
        self.hbox2.Add(scrolled_panel, flag=wx.EXPAND)
        scrolled_panel.SetSizer(vbox2)
        
        vbox3 = wx.BoxSizer(wx.VERTICAL)
        st = wx.StaticText(self.panel, label='Hello World!')
        st.Wrap(1000)
        vbox3.Add(st, flag=wx.EXPAND)
        self.hbox2.Add(vbox3, flag=wx.EXPAND)
        
        scrolled_panel.SetAutoLayout(1)
        scrolled_panel.SetupScrolling(scroll_x=False)
        #scrolled_self.panel.ShowScrollbars(wx.SHOW_SB_NEVER,wx.SHOW_SB_NEVER)
        
        
        self.panel.SetSizer(top_layer_vbox)
        
    def add_url(self, event):
        entry = wx.TextEntryDialog(self.panel, 'Add URL: ', '')
        entry.ShowModal()
        result = entry.GetValue()
        parsed = urlparse(result)
        # all cased url inputs
        """if not bool(parsed.scheme):
            parsed._replace(**{'scheme' : 'http'})
            parsed = urlparse(parsed.geturl())"""
        self.listbox.Append(result)
        
    def display(self, event):
        url = self.listbox.GetString(self.listbox.GetSelection())
        self.feed_page = rss.FeedPage(url)
        self.hbox2.Hide(1)
        """for i in range(5):
            st = ArticleBox(scrolled_panel, description='Article #' + str(i))
            vbox2.Add(st.get_description(), proportion=1, flag=wx.EXPAND | wx.BOTTOM, border=5)
        """
        print self.feed_page.feed.entries[0].title

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