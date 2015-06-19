# -*- coding: utf-8 -*-
__author__ = 'last5bits'

import urllib.request as req
import re

from Subcategory import Subcategory
from utils import html_decode

class Category:
    'Категория товаров: пистолет, винтовка и т.п.'

    def __init__(self, url):
        self.url = url
        html = self.get_html(url)

        # Добавить имя категории
        self.xml_str += '<category name="%s">' % self.get_name(html)

        # Добавить XML подкатегорий
        for url_and_image in self.get_subcategory_urls_and_images(html):
            prefix = 'http://www.air-gun.ru/'
            url =  prefix + html_decode(url_and_image[0])
            image = prefix + url_and_image[1]
            subcategory = Subcategory(url, image)
            self.xml_str += subcategory.get_xml_str()

        self.xml_str += '</category>'

    def get_xml_str(self):
        return self.xml_str

    def get_html(self, url):
        return req.urlopen(url).readall()

    def get_name(self, html):
        match = re.search('<title>(.+)<\/title>', str(html, "cp1251"))
        return match.group(1)

    def get_subcategory_urls_and_images(self, html):
        'Возвращает список кортежей: URL страницы + URL картинки'

        res = []
        for match in re.finditer("<a href='(.+)'>\s*<img src='(images\/podcateg\/\d+.jpg)'", str(html, "cp1251")):
            url, image = match.group(1), match.group(2)
            res.append((url, image))

        return res

    xml_str = ''
