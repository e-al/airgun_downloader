__author__ = 'last5bits'

from Category import Category

class Airgun:
    'Класс самого верхнего уровня для парсинга air-gun.ru'

    def __init__(self):
        self.xml_str += '<warehouse>'

        for url in self.category_urls:
            category = Category(url)
            self.xml_str += category.get_xml_str()

        self.xml_str += '</warehouse>'

    def get_xml_str(self):
        return self.xml_str

    category_urls = [
        # Пистолеты
        'http://www.air-gun.ru/index.php?m_id=1&op_cat=1&r_id=1&desc=pnevmaticheskie_pistoleti'
        # Винтовки
        # , 'http://www.air-gun.ru/index.php?m_id=2&op_cat=1&r_id=2&desc=Vintovki_pnevmaticheskie'
        # # Оптика / ЛЦУ
        # , 'http://www.air-gun.ru/index.php?m_id=18&op_cat=1&r_id=18&desc=Optika_/_LTsU'
        # # Кобуры, чехлы, кейсы
        # , 'http://www.air-gun.ru/index.php?m_id=19&op_cat=1&r_id=19&desc=Koburi,_chehli,_keysi'
    ]

    xml_str = ''
