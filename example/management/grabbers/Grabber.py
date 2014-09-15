# -*- coding: utf-8 -*-
import re
import sys
from datetime import datetime
from selenium import webdriver
from yandex_maps import api
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

reload(sys)
sys.setdefaultencoding('utf8')


class Grabber:
    def __init__(self, verbose, browser):
        self.verbose = verbose
        self.set_driver(browser)

    def set_driver(self, browser, options=None):
        if browser == 'phantomjs':
            if options is None:
                options = [['--load-images=false']]

            if options == 0:
                self.driver = webdriver.PhantomJS()
            else:
                self.driver = webdriver.PhantomJS(service_args=options[0])
        elif browser == 'firefox':
            if options is None:
                options = [['permissions.default.stylesheet', 2],
                           ['permissions.default.image', 2],
                           ['dom.ipc.plugins.enabled.libflashplayer.so', 'false'],
                           ['browser.download.folderList', 2],
                           ['javascript.enabled', 'false']]

            if options == 0:
                self.driver = webdriver.Firefox()
            else:
                firefox_profile = webdriver.FirefoxProfile()
                for option in options:
                    firefox_profile.set_preference(option[0], option[1])
                self.driver = webdriver.Firefox(firefox_profile=firefox_profile)

    def clean_array(self, template, arr):
        for i in range(len(arr)-1, 0, -1):
            text = arr[i].text
            if text != re.sub(template, '', text):
                arr.pop(i)

    def get_parallel_attribute(self, arr_1, arr_2, value):
        for el in arr_1:
            if el.text == value:
                return arr_2[arr_1.index(el)].text.lower()
        return 0

    def get_point(self, address):
        api_key = 'AL58ZlIBAAAA7Xs2NwIANDolptueIwOHHYvb76TmuGgXIu4AAAAAAAAAAAAuO3HCoZ2VUAPtAsm6-MOrhoGN-w=='
        pos = api.geocode(api_key, u'Москва ' + address)
        if pos[0] is None:
            return None
        return {'x': float(pos[0]), 'y': float(pos[1])}

    def print_log(self, time, expression='{0:d}', args=[]):
        args.insert(0, (datetime.now() - time).seconds)
        print expression.format(*args)

    def get_or_create(self, object, **args):
        try:
            return object.objects.get(**args)
        except ObjectDoesNotExist:
            return object(**args).save()
        except MultipleObjectsReturned:
            return object.objects.filter(**args)[0]