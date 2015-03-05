import wx
import feed
import fparser
import wx.html as html
import wx.html2
from goose import Goose
from textwrap import wrap
from threading import Thread
from wx.lib.pubsub import pub
# Testing module(s)
import requests
import json

class OGLEFrame(wx.Frame):
	"""Main Frame holding the panel"""

	def __init__(self, *args, **kwargs):
		"""Create OGLEFrame"""
		wx.Frame.__init__(self, *args, **kwargs)

		# Create feed database
		self.parsedfeed = fparser.FParser()

		# Set optimized size
		self.SetSize((1400, 800))

		# Build the menu bar HERE!
		#
		#

		# Add splitter
		self.splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
		# Add the Panels
		self.right_browser_panel = OGLERightBrowserPanel(self.splitter)
		self.right_parsed_panel = OGLERightBrowserPanel(self.splitter)
		self.left_panel = OGLELeftPanel(self.splitter)
		top_panel = OGLETopPanel(self)

		self.right_browser_panel.Hide()

		# Split the frame
		self.splitter.SplitVertically(self.left_panel, self.right_parsed_panel)
		self.splitter.SetMinimumPaneSize(600)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(top_panel, flag=wx.EXPAND)
		vbox.Add(self.splitter, proportion=1, flag=wx.EXPAND)
		self.SetSizer(vbox)

		# Bind add button to click event
		self.Bind(wx.EVT_BUTTON, self.OnButton_AddSource, top_panel.add_button)
		# Bind source list box to listbox event
		self.Bind(wx.EVT_LISTBOX, self.OnClick_SourceListBox, self.left_panel.source_listbox)
		# Bind Switch window button to click event
		self.Bind(wx.EVT_BUTTON, self.OnButton_SwitchWindow, top_panel.switch_button)
		# Bind article list box to listbox event
		self.Bind(wx.EVT_LISTBOX, self.OnClick_ArticleListBox, self.left_panel.article_listbox)

		self.Center() # Center the GUI on screen

		# testing
		# title = 'The White Winter Home Screen'
		# summary = "You may not be able to tell in some places, but we're right in the middle of winter. If you need a reminder beyond your window, this peacefully white home screen will make you feel winter's chill." \
		# 	"This design is made for both Themer and Zooper widgets. You can download the Themer file from the source link below and install by following these steps:" \
		# 	"Move the .zip to sdcard0 > MyColorScreen > Themer > Exported > zip (Your initial location may vary.)"
		# html_string = '<div align="left" style="margin:10px;"><font size=3 face="arial, sans-serif"><b>%s</b></div></font>' % title
		# html_string += '<div align="left"><font size=3 face="arial, sans-serif">%s</div></font>' % summary
		# self.right_parsed_panel.simple_browser.SetPage(html_string, '')

	def OnButton_AddSource(self, event):
		entry = wx.TextEntryDialog(None, 'Add Source', '')
		entry.ShowModal()
		url = entry.GetValue()
		# Check for http://
		if '://' not in url:
			url = 'http://' + url
		
		# Create Feed
		try:
			f = feed.FeedPage(url).feed
		except:
			raise Exception('Provided url does not contain any feed')
		# Update source listbox
		self.left_panel.source_listbox.add_source(url)
		# Pasing the feed
		self.parsedfeed.feed_update(url, f)
		for data in self.parsedfeed.get_data(url):
			article_url = data['link']
			g = Goose()
			article = g.extract(url=article_url)
			try:
				data['description'] = article.cleaned_text
			except:
				data['description'] = None
			try:
				data['image'] = article.top_image.src
			except:
				data['image'] = None

	def OnClick_SourceListBox(self, event):
		id = self.left_panel.source_listbox.data[event.GetSelection()]
		self.left_panel.article_listbox.update(self.parsedfeed.get_data(id))

	def OnButton_SwitchWindow(self, event):
		if self.right_browser_panel.IsShown():
			self.splitter.ReplaceWindow(self.right_browser_panel, self.right_parsed_panel)
			self.right_parsed_panel.Show()
			self.right_browser_panel.Hide()
		else:
			self.splitter.ReplaceWindow(self.right_parsed_panel, self.right_browser_panel)
			self.right_parsed_panel.Hide()
			self.right_browser_panel.Show()
			url = self.left_panel.article_listbox.data[self.left_panel.article_listbox.GetSelection()]['link']
			if self._compare_url(url):
				self.right_browser_panel.simple_browser.LoadURL(url)
				# Re-update url in case of redirect link
				#self.left_panel.article_listbox.data[self.left_panel.article_listbox.GetSelection()]['link'] = self.right_browser_panel.simple_browser.GetCurrentURL()
		self.Layout()

	def OnClick_ArticleListBox(self, event):
		data = self.left_panel.article_listbox.data[event.GetSelection()]
		title = data['title']
		image = data['image']
		description = data['description']
		if self.right_browser_panel.IsShown():
			url = data['link']
			if self._compare_url(url):
				self.right_browser_panel.simple_browser.LoadURL(url)
				# Re-update url in case of redirect link
				#self.left_panel.article_listbox.data[self.left_panel.article_listbox.GetSelection()]['link'] = self.right_browser_panel.simple_browser.GetCurrentURL()
		# Format title
		html_string = '<div style="margin:30"><h1 style="font-family:arial, sans-serif;">' + title + '</h1>'
		# Format image if exists
		if image:
			html_string += '<div align="center"><img src=' + image + ' style="max-width:100%; height:auto;"></div>'
		# Format description if exists
		if description:
			html_string += '<p style="font-family:arial, sans-serif;">' + description.replace('\n', '<br />') + '</p></div>'
		
		self.right_parsed_panel.simple_browser.SetPage(html_string, '')

	def _compare_url(self, url):
		"""
		Compare url from listbox and url of the currently displayed document
		url: url that is compared to current url
		Returns True if they are different
		"""
		current_url = self.right_browser_panel.simple_browser.GetCurrentURL()

		if (url != current_url):
			return True
		else:
			return False

class OGLETopPanel(wx.Panel):
	def __init__(self, parent, *args, **kwargs):
		wx.Panel.__init__(self, parent, *args, **kwargs)

		self.parent = parent
        
        # Create Logo
        # png = wx.Image(ogle.png, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
#         wx.StaticBitmap(self, -1, png, (10, 5), (png.GetWidth(), png.GetHeight()))
		# Create a ADD source button
		self.add_button = wx.Button(self, id=wx.ID_ADD, label='Add')
		# Create a SWITCH window button
		self.switch_button = wx.Button(self, label='Mode')

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(self.add_button, flag=wx.ALL, border=10)
		hbox.Add(self.switch_button, flag=wx.ALL, border=10)

		self.SetSizer(hbox)

class OGLERightParsedPanel(wx.Panel):
	"""
	The OGLE right Panel containing HtmlWindow rendering parsed text, and a main image
	"""
	def __init__(self, parent, *args, **kwargs):
		wx.Panel.__init__(self, parent, *args, **kwargs)

		self.parent = parent

		# Create a HtmlWindow
		self.htmlwindow = html.HtmlWindow(self)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.htmlwindow, proportion=1, flag=wx.EXPAND)
		self.SetSizer(sizer)

		#self.htmlwindow.SetPage( Html string HERE!! )
		#wx.InitAllImageHandlers()
		#self.htmlwindow.SetPage(requests.get('http://lifehacker.com').content)
		self.htmlwindow.SetPage('<p> HELLO WORLD v3 :DDDD </p>')

class OGLERightBrowserPanel(wx.Panel):
	"""
	The OGLE right Panel containing WebView Widget as a simple browser
	"""
	def __init__(self, parent, *args, **kwargs):
		"""Create a simeple browser"""
		wx.Panel.__init__(self, parent, *args, **kwargs)

		self.parent = parent
		# Create a simeple browser
		self.simple_browser = wx.html2.WebView.New(self)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.simple_browser, proportion=1, flag=wx.EXPAND|wx.ALL, border=7)
		self.SetSizer(sizer)

		# Testing purposes --------------
		#self.simple_browser.LoadURL('http://Techcrunch.com')
		#url = 'http://lifehacker.com/some-brands-and-stores-give-you-double-your-money-back-1679981339'
		#g = Goose()
		#article = g.extract(url=url)
		#self.simple_browser.SetPage('<img src=' + article.top_image.src + '>', '')

class OGLELeftPanel(wx.Panel):
	"""The OGLE left Panel containing 2 listboxes"""

	def __init__(self, parent, *args, **kwargs):
		"""Create OGLEPanel"""
		wx.Panel.__init__(self, parent, *args, **kwargs)

		self.parent = parent

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		self.SetSizer(hbox)

		# Create source_listbox
		self.source_listbox = SourceListBox(self)

		# For testing purposes -------------
		#source = ['Lifehacker', 'Digg', 'Mashable', 'Techcrunch', 'Venturebeat']
		#self.source_listbox.add_source(*source)
		# ----------------------------------

		hbox.Add(self.source_listbox, proportion=1, flag=wx.EXPAND|wx.ALL, border=7)

		# Create article_listbox
		self.article_listbox = ArticleListBox(self)

		# For testing purposes -------------
		#self.article_listbox.update(feed.FeedPage('http://lifehacker.com').feed.entries)
		# ----------------------------------

		hbox.Add(self.article_listbox, proportion=7, flag=wx.EXPAND|wx.ALL, border=7)

class SourceListBox(wx.HtmlListBox):
	"""Custom HtmlListBox holding a list of sources/URL's"""
	def __init__(self, parent, *args, **kwargs):
		# Set its size too??
		wx.HtmlListBox.__init__(self, parent, *args, **kwargs)
		self.data = []
		self.SetItemCount(len(self.data))

		self.SetMinSize((190, 0)) # Set min size
		self.SetMargins((5, 5)) # Set margins horizontally & vertically

	def OnGetItem(self, n):
		# Center align title
		return '<div align="left"><font size=4 face="arial, sans-serif">%s</div></font>' % self.data[n]

	def add_source(self, *args):
		# Check for any duplicated
		for source in args:
			# Encode any unicode text
			encoded_source = source.encode('utf-8')
			if (encoded_source not in self.data):
				self.data.append(encoded_source)
		# Also sorted by alphabetic order
		# Only works for ASCll
		self.data.sort(key=str.lower)
		self.SetItemCount(len(self.data))
		self.Refresh()

class ArticleListBox(wx.HtmlListBox):
	"""Custom HtmlListBox holding a list of article's summaries"""
	def __init__(self, parent, *args, **kwargs):
		wx.HtmlListBox.__init__(self, parent, *args, **kwargs)
		self.data = []
		self.SetItemCount(len(self.data))

		self.SetMargins((10, 10))

	def OnGetItem(self, n):
		title = self.data[n]['title']
		description = self.data[n]['description']
		# Format title
		html_string = '<div align="left"><font size=3 face="arial, sans-serif"><b>%s</b></div></font>' % title
		# Format description if exists
		if description:
			description = wrap(description, 220)[0].rstrip('.') + '...'
			html_string += '<div align="left"><font size=3 face="arial, sans-serif">%s</div></font>' % description
		return html_string
		#img = wx.Image(name='apple')
		#return img.LoadStream(requests.get('https://cdn1.iconfinder.com/data/icons/simple-icons/4096/apple-4096-black.png'))
		#return "<img src='apple.png'>"

	def update(self, feed):
		self.data = feed
		self.SetItemCount(len(self.data))
		self.Refresh()

class ExtractorThread(Thread):
	"""Thread class running Goose extractor"""
	def __init__(self, feed):
		"""Create ExtractorThread"""
		Thread.__init__(self)
		self.feed = feed
		self.start() # start the thread upon initiated

	def run(self):
		for data in self.feed:
			article_url = data['link']
			g = Goose()
			article = g.extract(url=article_url)
			try:
				data['description'] = article.cleaned_text
			except:
				data['description'] = None
			try:
				data['image'] = article.top_image.src
			except:
				data['image'] = None

if __name__ == '__main__':
	app = wx.App()
	mainframe = OGLEFrame(None, title='OGLE')
	mainframe.Show()
	app.MainLoop()