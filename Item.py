__author__ = 'e-al'

import re
import urllib
import urllib.request
from xml.sax.saxutils import escape

class Item:
    """Товар: элемент подкатегории, т.е. конкретная модель пистолета, винтовки, прицела, и т.д"""

    def __init__(self, url):
        opener = urllib.request.urlopen(url)
        page_source = opener.read().decode("cp1251")

        base_url = "http://air-gun.ru/"

        self.title = self.get_title(page_source)
        self.article = self.get_article(page_source)
        self.id = re.search('\?id=([0-9]+)', url).group(1)
        self.img_url = self.get_main_image_url(base_url, self.id)
        self.img_urls = self.get_all_image_urls(page_source, base_url, self.id)
        self.price = self.get_price(page_source)
        self.description = self.get_description(page_source)
        self.characteristics = self.get_characteristics(page_source)

    def get_title(self, page_source):
        title_re = re.compile('<title>(?P<title>.+?)</title>')
        return title_re.search(page_source).group("title").strip()

    def get_article(self, page_source):
        article_re = re.compile('Артикул:\s(?P<article>.+?)(?=</font>)')
        match = article_re.search(page_source)
        return "" if not match else match.group("article")

    def get_main_image_url(self, base_url, id):
        return base_url + "images/big/" + id + ".jpg"

    def get_all_image_urls(self, page_source, base_url, id):
        img_re = re.compile('<a\shref="(?P<path>images/big/' + id + '/[0-9]+?\.jpg)"\sclass="highslide"')
        urls = []
        for match in img_re.finditer(page_source):
            path = match.group("path")
            urls.append(base_url + path)
        return urls

    def get_price(self, page_source):
        price_re = re.compile('<div align="center"><strong><font size=4 color="B10000">(<h3><strike>.+?</strike></h3>)?'
                              '(?P<price>[0-9]+?)\sруб\.')
        match = price_re.search(page_source)
        return 0 if not match else match.group("price")

    def get_description(self, page_source):
        desc_re = re.compile('<strong>Описание:</strong><br><br>\s*'
                             '(<.*?>)*?(?P<desc>(?s).*?)\s*(<.*?>)*?(<center>|</font>)')
        match = desc_re.search(page_source)
        return "" if not match or not len (match.group("desc")) else escape(match.group("desc"))

    def get_characteristics(self, page_source):
        char_re = re.compile('<li class="active"><a href="#tab1">Характеристики</a>')
        if not char_re.search(page_source):
            return None
        char_re = re.compile("<td height='20' class='sm3' width='220' style='padding-left:5px; padding-top:2px; "
                             "padding-bottom:2px; border-top: solid 1px #d5d5d5;'>(?P<name>.+?):</td>\s*?<td class='sm4' "
                             "width='220' style='padding-left:5px; border-left: solid 1px #d5d5d5; padding-top:2px; "
                             "padding-bottom:2px; border-top: solid 1px #d5d5d5;'><strong>(?P<val>.*?)</strong>")
        chars = dict()
        for match in char_re.finditer(page_source):
            name, value = self.xml_escape(match.group("name")), self.xml_escape(match.group("val"))
            chars[name] = value
        return chars

    def get_desc_xml(self):
        return "<desc>{0}</desc>".format(self.xml_escape(self.description))

    def get_characteristics_xml(self):
        if not self.characteristics:
            return ""
        res_list = []
        for name, val in self.characteristics.items():
            res_list.append('<char name="{0}" val="{1}"/>'.format(escape(name), escape(val)))
        return "".join(res_list)

    def get_images_xml(self):
        if not len(self.img_urls):
            return ""
        res_list = []
        for url in self.img_urls:
            res_list.append('<img>{0}</img>'.format(url))
        return "".join(res_list)

    def xml_escape(self, str):
        return escape(str.replace("\n", " ").replace("\r", "").replace("\"", "&quot"))

    def get_xml_str(self):
        item_attrs = 'name="{0}" art="{1}" price="{2}" img="{3}"'.format(self.xml_escape(self.title)
                                                                         , self.xml_escape(self.article)
                                                                         , "Нет в наличии" if not self.price else self.price
                                                                         , self.img_url)

        return "<item {0}>{1}{2}{3}</item>".format(item_attrs, self.get_desc_xml()
                                                   , self.get_characteristics_xml()
                                                   , self.get_images_xml())
