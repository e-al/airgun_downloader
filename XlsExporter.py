__author__ = 'e-al'
import xml.etree.ElementTree as etree
import xlsxwriter

class XlsExporter:
    """Класс предназначен для экспортирования XML с товарами в таблицы XLS

    В конструктор передается два параметра - имя входного файла, сформированного скриптом Airgun.py
    и имя выходного файла XLS, в который требуется внести изменения
    """

    def __init__(self, xmlfilename, out_xls):
        self.xml = xmlfilename
        self.out_xls = out_xls
        self.workbook = xlsxwriter.Workbook(out_xls)
        self.products_fields_positions = dict()
        self.categories_fields_positions = dict()
        self.images_fields_positions = dict()
        self.attributes_fields_positions = dict()

        self.categories_worksheet = None
        self.products_worksheet = None
        self.images_worksheet = None
        self.attributes_worksheet = None

        self.setup_categories_worksheet()
        self.setup_products_worksheet()
        self.setup_images_worksheet()
        self.setup_attributes_worksheet()


    def setup_products_worksheet(self):
        self.products_worksheet = ws = self.workbook.add_worksheet('Products')
        fields = ['product_id','name','categories','sku','upc','ean','jan','isbn','mpn','location','quantity','model'
            ,'manufacturer','image_name' ,'requires shipping','price','points','date_added','date_modified'
            ,'date_available','weight','unit','length','width','height','length unit','status\nenabled', 'tax_class_id'
            , 'viewed', 'language_id', 'seo_keyword', 'description', 'meta_description', 'meta_keywords', 'seo_title'
            , 'seo_h1', 'stock_status_id', 'store_ids', 'layout', 'related_ids', 'tags', 'sort_order', 'substract'
            , 'minimum'
                  ]
        i = 0
        for field in fields:
            self.products_fields_positions[field] = i
            i += 1

        ws.write_row(0, 0, fields)

    def setup_categories_worksheet(self):
        self.categories_worksheet = ws = self.workbook.add_worksheet('Categories')
        fields = ['category_id', 'parent_id', 'name', 'top', 'columns', 'sort_order', 'image_name', 'date_added'
            , 'date_modified', 'language_id', 'seo_keyword', 'description', 'meta_description', 'meta_keywords'
            , 'seo_title', 'seo_h1', 'store_ids', 'layout', 'status\nenabled']

        i = 0
        for field in fields:
            self.categories_fields_positions[field] = i
            i += 1

        ws.write_row(0, 0, fields)

    def setup_images_worksheet(self):
        self.images_worksheet = ws = self.workbook.add_worksheet('AdditionalImages')
        fields = ['product_id', 'image', 'sort_order']

        i = 0
        for field in fields:
            self.images_fields_positions[field] = i
            i += 1

        ws.write_row(0, 0, fields)

    def setup_attributes_worksheet(self):
        self.attributes_worksheet = ws = self.workbook.add_worksheet('Attributes')
        fields = ['product_id', 'language_id', 'attribute_group', 'attribute_name', 'text']

        i = 0
        for field in fields:
            self.attributes_fields_positions[field] = i
            i += 1

        ws.write_row(0, 0, fields)

    def export(self):
        tree = etree.parse(self.xml)
        root = tree.getroot()

        category_id = 0
        item_id = 1
        images_processed = 0
        chars_processed = 0
        for category in root:
            category_id += 1
            self.categories_worksheet.write_number(category_id, self.categories_fields_positions["category_id"]
                                                   , category_id)
            self.categories_worksheet.write(category_id, self.categories_fields_positions["name"]
                                            , category.attrib["name"])
            self.categories_worksheet.write_number(category_id, self.categories_fields_positions["parent_id"], 0)
            self.categories_worksheet.write(category_id, self.categories_fields_positions["top"], "true")
            self.categories_worksheet.write(category_id, self.categories_fields_positions["status\nenabled"], "true")
            parent_cat = category_id
            for subcat in category:
                category_id += 1
                self.categories_worksheet.write_number(category_id, self.categories_fields_positions["category_id"]
                                                       , category_id)
                self.categories_worksheet.write_number(category_id, self.categories_fields_positions["parent_id"]
                                                       , parent_cat)
                self.categories_worksheet.write(category_id, self.categories_fields_positions["name"]
                                                , subcat.attrib["name"])
                self.categories_worksheet.write(category_id, self.categories_fields_positions["image_name"]
                                                , subcat.attrib["img"])
                self.categories_worksheet.write(category_id, self.categories_fields_positions["top"], "false")
                self.categories_worksheet.write(category_id, self.categories_fields_positions["status\nenabled"]
                                                , "true")
                for item in subcat:
                    imgs, chars = self.process_item(item, item_id, category_id, images_processed, chars_processed, subcat)
                    images_processed += imgs
                    chars_processed += chars
                    item_id += 1

        self.workbook.close()

    def process_item(self, item, item_id, category_id, images_processed, chars_processed, subcat):
        self.products_worksheet.write_number(item_id, self.products_fields_positions["product_id"], item_id)
        self.products_worksheet.write(item_id, self.products_fields_positions["name"], item.attrib["name"])
        self.products_worksheet.write(item_id, self.products_fields_positions["categories"], category_id)
        self.products_worksheet.write(item_id, self.products_fields_positions["manufacturer"], subcat.attrib["name"])
        self.products_worksheet.write(item_id, self.products_fields_positions["image_name"], item.attrib["img"])
        price = 0 if not item.attrib["price"].isnumeric() else item.attrib["price"]
        self.products_worksheet.write_number(item_id, self.products_fields_positions["price"], int(price))
        self.products_worksheet.write(item_id, self.products_fields_positions["description"]
                                      , item.findall("desc")[0].text)
        self.products_worksheet.write(category_id, self.products_fields_positions["status\nenabled"], "true")

        images = item.findall("img")
        for img in images:
            self.images_worksheet.write_row(images_processed + 1, 0, [item_id, img.text, 0])
            images_processed += 1

        chars = item.findall("char")

        # 1 - id языка по умолчанию
        language_id = 1
        for char in chars:
            # нет возможности различать поля attribute_group и attribute_name, поэтому делаем их одинаковыми
            self.attributes_worksheet.write_row(chars_processed + 1, 0, [item_id, language_id, char.attrib["name"]
                , char.attrib["name"], char.attrib["val"]])
            chars_processed += 1

        return len(images), len(chars)
