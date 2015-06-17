__author__ = 'last5bits'

import warnings
import urllib.request as req
import re
import os

from Subcategory import Subcategory

class Category:
    'Категория товаров: пистолет, винтовка и т.п.'

    def __init__(self, url):
        self.url = url
        html = self.get_html(url)

        # Добавить имя категории
        self.xml_str += '<category name="%s">' % self.get_name(html) + os.linesep

        # Добавить XML подкатегорий
        for sub_url in self.get_subcategory_urls(html):
            subcategory = Subcategory(sub_url)
            self.xml_str += subcategory.get_xml_str()

        self.xml_str += '</category>' + os.linesep

    def get_xml_str(self):
        return self.xml_str

    def get_html(self, url):
        return req.urlopen(url).readall()

    def get_name(self, html):
        match = re.search('<title>(.+)<\/title>', str(html, "cp1251"))
        return match.group(1)

    def get_subcategory_urls(self, html):
        warnings.warn('Not implemented yet')
        return html

    xml_str = ''
