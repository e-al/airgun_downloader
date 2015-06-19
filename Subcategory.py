# -*- coding: utf-8 -*-
__author__ = 'e-al'

import urllib.request as req
import re

from Item import Item
from utils import html_decode
from xml.dom.minidom import parseString

class Subcategory:
    'Подкатегория товаров. Например, для пистолетов: Аникс, Umarex, Ижевск и т.д.'

    def __init__(self, url, img_url):
        first_html = self.get_html(url)

        self.xml_str += '<subcat name="%s" img="%s">' % (self.get_name(first_html), img_url)

        # Первая страница
        for url in self.get_items_urls(first_html):
            item = Item(url)
            self.xml_str += item.get_xml_str()

        # Остальные страницы
        for page_url in self.get_pages_urls(first_html):
            html = self.get_html(page_url)
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

    def get_pages_urls(self, html):
        urls = []
        for match in re.finditer('<a href="(index\.php\?m_id=\d+&amp;pcat=\d+&amp;op_cat=\d+&amp;st=\d+)">', str(html, "cp1251")):
            urls.append('http://www.air-gun.ru/' + html_decode(match.group(1)))

        return urls

    xml_str = ''
