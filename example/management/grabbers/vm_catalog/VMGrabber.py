# -*- coding: utf-8 -*-
from __future__ import with_statement
from random import random
import signal
from contextlib import contextmanager
from urllib2 import URLError
from httplib import BadStatusLine
from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import F
from example.models.all import \
    AiVirtuemartCategoriesRuRu, \
    AiVirtuemartCategories, \
    AiVirtuemartCategoryCategories, \
    AiVirtuemartManufacturers, \
    AiVirtuemartManufacturersRuRu, AiVirtuemartMedias, AiVirtuemartProductsRuRu, AiVirtuemartProductCategories, AiVirtuemartProducts, AiVirtuemartProductMedias, AiVirtuemartProductPrices, AiVirtuemartProductManufacturers

from selenium.common.exceptions import \
    ErrorInResponseException, \
    WebDriverException, \
    ImeActivationFailedException

from example.management.grabbers.Grabber import *


# ignore exception
class TimeoutException(Exception):
    pass


# create exception handler
@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException, 'Timed out!'

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


class VMGrabber(Grabber):
    def __init__(self, verbose=0, browser='phantomjs'):
        Grabber.__init__(self, verbose, browser)
        self.pages = []

    def start(self, queue, grabber_cls, browser_name):
        start = True
        while True:
            job = queue.get()
            if job is None:
                break
            while 1:
                try:
                    try:
                        if start:
                            with time_limit(15):
                                grabber = grabber_cls(0, browser_name)
                                start = False
                        grabber.grab_brands(job)
                        queue.task_done()
                        break

                    except TimeoutException:
                        print "Error:", sys.exc_info()[0]
                    except (ErrorInResponseException, ImeActivationFailedException, KeyboardInterrupt):
                        print "Error: %s url: %s" % (sys.exc_info()[0], grabber.driver.current_url)
                        grabber.driver.quit()
                        exit(0)
                    except (BadStatusLine, URLError):
                        try:
                            grabber.driver.quit()
                        except UnboundLocalError:
                            grabber = grabber_cls(0, browser_name)
                        print "Error:", sys.exc_info()[0]
                except (WebDriverException, URLError, BadStatusLine):
                    try:
                        grabber.driver.quit()
                    except UnboundLocalError:
                        grabber = grabber_cls(0, browser_name)
        grabber.driver.quit()
        queue.task_done()

    def set_pages(self, elms):
        pages = []
        for elm in elms:
            href = elm.get_attribute('href')
            pages.append(href)
        return pages

    def get_or_create_manufacture(self, m_name):
        obj = AiVirtuemartManufacturersRuRu
        try:
            return obj.objects.get(**{'mf_name': m_name})
        except ObjectDoesNotExist:
            try:
                id = AiVirtuemartManufacturers.objects.latest(
                    'virtuemart_manufacturer_id').virtuemart_manufacturer_id + 1
            except ObjectDoesNotExist:
                id = 0

            AiVirtuemartManufacturers.objects.create(
                **{'virtuemart_manufacturer_id': id,
                   'hits': 0,
                   'published': 1,
                   'created_by': 0,
                   'created_on': datetime.now(),
                   'modified_by': 0,
                   'modified_on': datetime.now(),
                   'locked_by': 0,
                   'locked_on': datetime.now()})

            for i in [",", "(", ")"]:
                m_name.replace(i, '')

            return obj.objects.create(
                **{'virtuemart_manufacturer_id': id,
                   'mf_name': m_name,
                   'slug': m_name.replace(' ', '-').lower()})
        except MultipleObjectsReturned:
            return obj.objects.filter(**{'mf_name': m_name})[0]

    def get_or_create_category(self, category_name):
        obj = AiVirtuemartCategoriesRuRu
        try:
            return obj.objects.get(**{'category_name': category_name})
        except ObjectDoesNotExist:
            try:
                id = AiVirtuemartCategories.objects.latest('virtuemart_category_id').virtuemart_category_id + 1
            except ObjectDoesNotExist:
                id = 0

            ordering = AiVirtuemartCategories.objects.latest('ordering').ordering + 1
            AiVirtuemartCategories.objects.create(**{'virtuemart_category_id': id, 'ordering': ordering})

            return obj.objects.create(
                **{'virtuemart_category_id': id,
                   'category_name': category_name,
                   'slug': category_name.replace(' ', '-').lower()})
        except MultipleObjectsReturned:
            return obj.objects.filter(**{'category_name': category_name})[0]

    def get_or_create_category_categories(self, parent_id, child_id):
        obj = AiVirtuemartCategoryCategories
        try:
            return obj.objects.get(**{'category_parent_id': parent_id,
                                      'category_child_id': child_id})
        except ObjectDoesNotExist:
            try:
                ordering = obj.objects.latest('ordering').ordering + 1
            except ObjectDoesNotExist:
                ordering = 0

            return obj.objects.create(
                **{'category_parent_id': parent_id,
                   'category_child_id': child_id,
                   'ordering': ordering})
        except MultipleObjectsReturned:
            return obj.objects.filter(**{'category_parent_id': parent_id,
                                         'category_child_id': child_id})[0]

    def get_or_create_media(self, img_path, type='product'):
        obj = AiVirtuemartMedias
        try:
            return obj.objects.get(**{'file_url': img_path})
        except ObjectDoesNotExist:
            while 1:
                try:
                    try:
                        id = AiVirtuemartMedias.objects.latest('virtuemart_media_id').virtuemart_media_id + 1
                    except ObjectDoesNotExist:
                        id = 0

                    return obj.objects.create(
                        **{'virtuemart_media_id': id,
                           'file_type': type,
                           'file_url': img_path,
                           'file_url_thumb': img_path})
                except IntegrityError:
                    print "product_id",
                    pass

        except MultipleObjectsReturned:
            return obj.objects.filter(**{'file_url': img_path})[0]

    def get_or_create_product(self, product_name, product_sku, product_desc, product_price=None, product_img_src=None):
        obj = AiVirtuemartProductsRuRu
        try:
            return obj.objects.get(**{'product_name': product_name})
        except ObjectDoesNotExist:
            while 1:
                try:
                    try:
                        id = AiVirtuemartProducts.objects.latest('virtuemart_product_id').virtuemart_product_id + 1
                    except ObjectDoesNotExist:
                        id = 0
                    # product
                    AiVirtuemartProducts.objects.create(**{'virtuemart_product_id': id, 'product_sku': product_sku})
                    break
                except IntegrityError:
                    print "media_id",
                    pass

            try:
                product = obj.objects.create(**{'product_name': product_name,
                                                'virtuemart_product_id': id,
                                                'product_desc': product_desc,
                                                'slug': product_name.replace(' ', '-').lower()})
            except IntegrityError:
                print "slug",
                product = obj.objects.create(**{'product_name': product_name,
                                                'virtuemart_product_id': id,
                                                'product_desc': product_desc,
                                                'slug': product_name.replace(' ', '-').lower() + str(
                                                    int(random() * 1000))})

            # prices
            AiVirtuemartProductPrices.objects.create(
                **{'virtuemart_product_id': id,
                   'product_price': int(product_price)})

            # media
            media = self.get_or_create_media(product_img_src)
            AiVirtuemartProductMedias.objects.create(**{'virtuemart_product_id': id,
                                                        'virtuemart_media_id': media.virtuemart_media_id,
                                                        'ordering': 0})
            return product
        except MultipleObjectsReturned:
            return obj.objects.filter(**{'product_name': product_name})[0]

    def save_manufactures(self, manufacturers):
        for manufacture_name in manufacturers:
            if manufacture_name:
                self.get_or_create_manufacture(manufacture_name)

    def save_products(self, products):
        for product in products:
            prdct = self.get_or_create_product(product['name'],
                                               product['sku'],
                                               product['description'],
                                               product['price'],
                                               product['img_path'])
            if product['category']:
                category = self.get_or_create_category(product['category'])
                self.get_or_create(AiVirtuemartCategoryCategories,
                                   **{'category_parent_id': product['parent_category_id'],
                                      'category_child_id': category.virtuemart_category_id})
                self.get_or_create(AiVirtuemartProductCategories,
                                   **{'virtuemart_product_id': prdct.virtuemart_product_id,
                                      'virtuemart_category_id': category.virtuemart_category_id,
                                      'ordering': 0})

            if product['brand']:
                manufacture = self.get_or_create_manufacture(product['brand'])
                self.get_or_create(AiVirtuemartProductManufacturers,
                                   **{'virtuemart_product_id': prdct.virtuemart_product_id,
                                      'virtuemart_manufacturer_id': manufacture.virtuemart_manufacturer_id})