from HTMLParser import HTMLParser

class RssParser(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        temp_list = ' '.join(self.fed).replace('\r', '').replace('  ', ' ').split('\n')
        temp_list = filter(lambda s: s != '\n', temp_list)
        return '\n\n'.join(temp_list)