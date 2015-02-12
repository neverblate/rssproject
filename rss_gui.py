import rss
from Tkinter import *

class Application():
    def __init__(self, master):
        
        url_entry = Entry(master)
        url_entry.pack(fill=X)
        url_entry.bind('<Return>', self.rss_write)
        
        scrollbar =Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.middle_text_area = Text(master, wrap=WORD, yscrollcommand=scrollbar.set, borderwidth=2, relief=RAISED, font=('Monaco', 16))
        self.middle_text_area.config(state=DISABLED)
        self.middle_text_area.pack(fill=BOTH, expand=1)
        scrollbar.config(command=self.middle_text_area.yview)
        
    def rss_write(self, event):
        try:
            rss_page = rss.RssPage(event.widget.get())

            titles, descriptions = rss_page.get_title(), rss_page.get_description()
        
            main_text = ''
            for i in range(len(titles)):
                main_text += titles[i].encode('utf-8')
                main_text += '\n\n'
                main_text += descriptions[i].encode('utf-8')
                main_text += '\n\n\n\n'
        
            self.middle_text_area.config(state='normal')
            self.middle_text_area.delete("1.0", END)
            self.middle_text_area.insert(INSERT, main_text)
            self.middle_text_area.config(state=DISABLED)
            print "VBCVBCVBC"
        except:
            self.middle_text_area.delete("1.0", END)
            self.middle_text_area.config(state=DISABLED)
            print "FGDGDF"
    
root = Tk()

app = Application(root)

root.mainloop()