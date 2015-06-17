__author__ = 'e-al'

import urllib.request as req
import re

from Item import Item

class Subcategory:
    'Подкатегория товаров. Например, для пистолетов: Аникс, Umarex, Ижевск и т.д.'

    def __init__(self, url, img_url):
        html = self.get_html(url)

        self.xml_str += '<subcat name="%s" img="%s">' % (self.get_name(html), img_url)
        for url in self.get_items_urls(html):
            item = Item(url)
            self.xml_str += item.get_xml_str()

        self.xml_str += '</subcat>'

    def get_xml_str(self):
        return self.xml_str

    def get_html(self, url):
        return req.urlopen(url).readall()

    def get_name(self, html):
        match = re.search('<title>(.+)<\/title>', str(html, "cp1251"))
        return match.group(1)

    def get_items_urls(self, html):
        urls = []
        for match in re.finditer('<br><a href="(show_image\.php\?id=\d+)"', str(html, "cp1251")):
            urls.append('http://www.air-gun.ru/' + match.group(1))

        return urls

    xml_str = ''
