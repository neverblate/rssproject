import wx
import wx.lib.stattext as ST
from wx.lib.wordwrap import wordwrap

class Application(wx.Frame):
    
    def __init__(self, parent, title, *args, **kwargs):
        super(Application, self).__init__(parent, title='What is my name, anyway?', size=(800,400))
        
        self.InitUI()
        self.Centre()
        self.Show()
    
    def InitUI(self):
        
        panel = wx.Panel(self)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        self.listbox = wx.ListBox(panel)
        
        vbox1 = wx.BoxSizer(wx.VERTICAL)   
        vbox1.Add(self.listbox, proportion=1, flag=wx.EXPAND)
        
        hbox.Add(vbox1, flag=wx.EXPAND)
        
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        # temp implt
        for i in range(5):
            st = ArticleBox(panel, "This is an example of static text \nHello World!Hello World!Hello World!Hello World!Hello World!")
            vbox2.Add(st.get_description(), proportion=1, flag=wx.EXPAND | wx.BOTTOM, border=5)
        hbox.Add(vbox2, flag=wx.EXPAND)
        
        vbox3 = wx.BoxSizer(wx.VERTICAL)
        st = wx.StaticText(panel, label='Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!')
        st.Wrap(1000)
        vbox3.Add(st, flag=wx.EXPAND)
        hbox.Add(vbox3, flag=wx.EXPAND)
        
        
        panel.SetSizer(hbox)

#might be removed
class ArticleBox():
    def __init__(self, parent, description='', url=''):
        parsed_description = wordwrap(description, 300, wx.ClientDC(parent))
        self.static_text = ST.GenStaticText(parent, -1, parsed_description, size=(300, 300))
        self.url = url
    
    def get_description(self):
        return self.static_text
        
    def get_url(self):
        return self.url
    
if __name__ == '__main__':
    app = wx.App()
    Application(None, title='rss needs name!')
    app.MainLoop()