# -*- coding: utf-8 -*-
from EventsGrabber import *


class KudaGoGrabber(EventsGrabber):
    def __init__(self, verbose=0, browser='phantomjs'):
        EventsGrabber.__init__(self, verbose, browser)

    def grab_count_of_pages(self, period):
        if period == 'future':
            url = 'http://kudago.com/msk/events/'
        else:
            url = 'http://kudago.com/msk/events/?date=past'
        self.driver.get(url)
        elm = self.driver.find_element_by_css_selector('nav.pagination')
        number_of_pages = int(elm.get_attribute('data-pages'))
        return number_of_pages

    def grab_pages_with_objects(self, period='future', start_page=0, number_of_pages=0):
        if self.verbose:
            start_time_point = datetime.now()

        self.pages = []
        self.events = []

        if period == 'future':
            url_pattern = 'http://kudago.com/msk/events/?page='
        else:
            url_pattern = 'http://kudago.com/msk/events/?date=past&page='

        page_number = start_page
        last_page = start_page + number_of_pages

        while 1:
            if self.verbose:
                time_point = datetime.now()

            self.driver.get(url_pattern + str(page_number))

            events_links = self.driver.find_elements_by_css_selector('header > h3 > a')
            self.set_pages(events_links)

            # log time ignores validate part
            if self.verbose:
                self.print_log(time_point, '{1:d}\ngrabbed page {2:d} in {0:d}\n{3:s}\n',
                               [len(self.pages), page_number, self.driver.current_url])

            page_number += 1

            # last page validate
            if number_of_pages != 0 and page_number == last_page:
                break
            if self.driver.find_element_by_class_name('load-more-button').get_attribute('hidden') is not None:
                break

        if self.verbose:
            self.print_log(start_time_point, 'grabbed {1:d} pages in {0:d} seconds\n', [page_number - start_page])

    def grab_events_pages(self, pages=None):
        if self.verbose:
            start_time_point = datetime.now()

        if pages is None:
            pages = self.pages

        for page in pages:
            if self.verbose:
                time_point = datetime.now()
                self.driver.get(page)
                print '%s\npage loading time: %d' % (page, (datetime.now() - time_point).seconds)
            else:
                self.driver.get(page)

            info_dds = self.driver.find_elements_by_css_selector('dl > dt > big')
            info_dts = self.driver.find_elements_by_css_selector('dl > dd')
            if len(info_dds) != len(info_dts):
                self.clean_array(u'^\s+|Смотреть на карте Яндекс|В календарь|\'\'|\s+$', info_dts)

            if self.get_parallel_attribute(info_dds, info_dts, u'СТИЛИ МУЗЫКИ') != 0:
                subjects = u'музыка'
            else:
                subjects = self.get_parallel_attribute(info_dds, info_dts, u'ВИД ПРЕДСТАВЛЕНИЯ')
                if subjects != 0:
                    subjects = subjects.split(' ')

            address = self.get_parallel_attribute(info_dds, info_dts, u'Адрес'.upper())
            if isinstance(address, basestring):
                address = address.replace(
                    u'© яндекссообщить об ошибке · условия использования', '')

            time_from = 0
            time_till = 0

            if self.get_parallel_attribute(info_dds, info_dts, u'Начнется'.upper()) != 0:
                time_from = self.string_to_date(self.get_parallel_attribute(info_dds, info_dts,
                                                                            u'Начнется'.upper()))
            else:
                if self.get_parallel_attribute(info_dds, info_dts, u'Начало'.upper()) != 0:
                    time_from = self.string_to_date(self.get_parallel_attribute(info_dds, info_dts,
                                                                                u'Начало'.upper()))
            if self.get_parallel_attribute(info_dds, info_dts, u'Закончится'.upper()) != 0:
                time_till = self.string_to_date(self.get_parallel_attribute(info_dds, info_dts,
                                                                            u'Закончится'.upper()))
            else:
                if self.get_parallel_attribute(info_dds, info_dts, u'Окончание'.upper()) != 0:
                    time_till = self.string_to_date(self.get_parallel_attribute(info_dds, info_dts,
                                                                                u'Окончание'.upper()))

            title = self.grab_value_via_try_except_by('header > h1')
            place = self.get_parallel_attribute(info_dds, info_dts, u'Место проведения'.upper())

            if isinstance(title, basestring):
                event = dict(title=title.lower(), subjects=subjects,
                             price=self.split_prices(
                                 self.get_parallel_attribute(info_dds, info_dts, u'Стоимость'.upper())),
                             place=place.lower() if isinstance(place, basestring) else 0,
                             address=address, href=page, duration={'from': time_from, 'till': time_till})
                self.events.append(event)

            if self.verbose:
                self.print_log(time_point, 'grabbed page in {0:d} seconds\n{1:f}%',
                               [float((pages.index(page) + 1)) / len(pages)])

        self.save(self.events)

        if self.verbose:
            self.print_log(start_time_point, 'grabbed {1:d} pages in {0:d} seconds', [len(self.pages)])