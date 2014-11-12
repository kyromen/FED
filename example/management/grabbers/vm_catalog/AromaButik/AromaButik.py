# -*- coding: utf-8 -*-
import copy
import urllib
from VMGrabber import *
import os.path


class AromaButik(VMGrabber):
    def __init__(self, verbose=0, browser='phantomjs'):
        VMGrabber.__init__(self, verbose, browser)

    def grab_count_of_pages(self):
        self.driver.get('http://www.aroma-butik.ru/catalog.php')

        elms = self.driver.find_elements_by_css_selector('.brand_list a')
        pages = self.set_pages(elms)

        return pages

    def grab_brands(self, pages):
        if self.verbose:
            start_time_point = datetime.now()

        for page in pages:
            if self.verbose:
                time_point = datetime.now()

            self.driver.get(page)

            elms = self.driver.find_elements_by_css_selector('.p_title a')
            self.grab_products(self.set_pages(elms))

            # log time ignores validate part
            if self.verbose:
                self.print_log(time_point, 'grabbed page {1:d} in {0:d}\n{2:s}\n',
                               [pages.index(page), self.driver.current_url])

        if self.verbose:
            self.print_log(start_time_point, 'grabbed {1:d} pages in {0:d} seconds\n', [len(pages)])

    def grab_products(self, pages):
        try:
            if self.verbose:
                start_time_point = datetime.now()

            products = []

            for page in pages:
                if self.verbose:
                    time_point = datetime.now()

                self.driver.get(page)

                name = self.driver.find_element_by_css_selector('.content > h1').text
                description = self.driver.find_element_by_css_selector('.p_descr span').text
                prdcts = self.driver.find_elements_by_css_selector('.c_table tr')

                lis = self.driver.find_elements_by_css_selector('.pd_prop li')

                product = {'description': description}

                for li in lis:
                    if re.match(u"Код товара: ", li.text):
                        attr = li.text.split(u"Код товара: ")[1]
                        product['sku'] = attr
                    elif re.match(u"Торговый дом: ", li.text):
                        attr = li.text.split(u"Торговый дом: ")[1]
                        product['brand'] = attr
                    elif re.match(u"Назначение: ", li.text):
                        attr = li.text.split(u"Назначение: ")[1]
                        if attr == "мужской":
                            product['category'] = "Мужские"
                        elif attr == "женский":
                            product['category'] = "Женские"
                        else:
                            print "ERROOOOOOR!!!!: " + attr
                    elif re.match(u"Семейства:", li.text):
                        attr = li.text.split(u"Семейства: ")[1]
                    elif re.match(u"Применение: ", li.text):
                        attr = li.text.split(u"Применение: ")[1]
                    elif re.match(u"Ноты аромата: ", li.text):
                        attr = li.text.split(u"Ноты аромата: ")[1]
                    elif re.match(u"Теги: ", li.text):
                        attr = li.text.split(u"Теги: ")[1]
                    elif re.match(u"Производство: ", li.text):
                        pass
                    elif re.match(u"Средняя оценка: ", li.text):
                        pass
                    else:
                        print li.text

                try:
                    product['name'] = name.split(' ' + product['brand'])[0]
                except IndexError:
                    product['name'] = name.split(product['brand'] + ' ')[1]

                img_src = self.driver.find_element_by_css_selector(".thumb img").get_attribute('src')
                name = re.split("/", img_src)[-1]

                product['img_path'] = "images/stories/virtuemart/product/" + name
                img_path = "//home//alex//workspace//VMGrabber//example//" \
                           "management//grabbers//vm_catalog//images//" \
                           + name
                if not os.path.isfile(img_path):
                    urllib.urlretrieve(img_src, img_path)

                for prd in prdcts:
                    product_ = copy.deepcopy(product)
                    name = prd.find_element_by_css_selector('th').text
                    price = prd.find_element_by_css_selector('span b').text

                    if "набор" in name:
                        product_['category'] = 'Набор'
                    elif "туалетная вода" in name:
                        product_['category'] = 'Туалетная вода'
                    elif "туалетные дух" in name:
                        product_['category'] = 'Туалетные духи'
                    elif "духи" in name:
                        product_['category'] = 'Духи'
                    elif "дезодорант" in name:
                        product_['category'] = 'Дезодорант'
                    elif "одеколон" in name:
                        product_['category'] = 'Одеколон'
                    else:
                        product_['category'] = 'Другое'

                    product_['parent_category_id'] = self.get_or_create_category(
                        product['category']).virtuemart_category_id

                    if product['category'] == "Мужские":
                        product_['category'] += "_м"

                    product_['price'] = price.split(' ')[0]
                    product_['name'] += " (" + name + ")"
                    products.append(product_)

                # log time ignores validate part
                if self.verbose:
                    self.print_log(time_point, 'grabbed page {1:d} in {0:d}\n{2:s}\n',
                                   [pages.index(page), self.driver.current_url])

            if self.verbose:
                self.print_log(start_time_point, 'grabbed {1:d} pages in {0:d} seconds\n', [len(pages)])
        except:
            print "Error:", sys.exc_info()[0]
            print self.driver.current_url

        self.save_products(products)
