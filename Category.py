__author__ = 'last5bits'

import warnings

from Subcategory import Subcategory

class Category:
    'Категория товаров: пистолет, винтовка и т.п.'

    def __init__(self, url):
        self.url = url
        html = self.get_html(url)
        for sub_url in self.get_subcategory_urls(html):
            subcategory = Subcategory(sub_url)
            self.xml_str += subcategory.get_xml_str()

    def get_xml_str(self):
        return self.xml_str

    def get_html(self, url):
        warnings.warn('Not implemented yet')
        return url

    def get_subcategory_urls(self, html):
        warnings.warn('Not implemented yet')
        return html

    xml_str = ''
