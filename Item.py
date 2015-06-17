__author__ = 'e-al'
import re
import urllib
import urllib.request

class Item:
    def __init__(self, url, base_url):
        opener = urllib.request.urlopen(url)
        page_source = opener.read().decode("cp1251")
        self.title = self.get_title(page_source)
        self.article = self.get_article(page_source)
        self.id = re.search('\?id=([0-9]+)', url).group(1)
        self.img_url = self.get_main_image_url(base_url, self.id)
        # self.img_urls = self.get_all_image_urls(page_source, base_url, self.title)

    def get_title(self, page_source):
        title_re = re.compile('<title>(?P<title>.+?)</title>')
        return title_re.search(page_source).group("title").strip()

    def get_article(self, page_source):
        article_re = re.compile('Артикул:\s(?P<article>.+?)(?=</font>)')
        return article_re.search(page_source).group("article")

    def get_main_image_url(self, base_url, id):
        if base_url[-1] != '/':
            base_url += '/'
        return base_url + "images/big/" + id+ ".jpg"


    def get_all_image_urls(self, page_source, base_url, title):
        pass
        # img_re = re.compile('<img\s+?src="images/big/(?P<filename>.*?)\.jpg"')#\s+?alt="' + title + '">')
        # urls = []
        # if base_url[-1] != '/':
        #     base_url += '/'
        # for match in img_re.finditer(page_source):
        #     fname = match.group("filename")
        #     urls.append(base_url + "images/big/" + fname)
        # return urls

    def get_xml_str(self):
        pass


item = Item("http://www.air-gun.ru/show_image.php?id=1801", "http://www.air-gun.ru")

print(item.title)
print(item.article)
print(item.img_url)

