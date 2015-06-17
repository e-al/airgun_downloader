__author__ = 'e-al'

import warnings
import urllib.request as req
import re
import os

class Subcategory:
    'Подкатегория товаров. Например, для пистолетов: Аникс, Umarex, Ижевск и т.д.'

    def __init__(self, url, img_url):
        html = self.get_html(url)

        self.xml_str += '<subcat name="%s" img="%s">' % (self.get_name(html), img_url) + os.linesep
        self.xml_str += '</subcat>' + os.linesep

    def get_xml_str(self):
        warnings.warn('Not implemented yet')
        return self.xml_str

    def get_html(self, url):
        return req.urlopen(url).readall()

    def get_name(self, html):
        match = re.search('<title>(.+)<\/title>', str(html, "cp1251"))
        return match.group(1)

    xml_str = ''
