# -*- coding: utf-8 -*-
from EventsGrabber import *


class TwoDoTwoGoGrabber(EventsGrabber):
    def __init__(self, verbose=0, browser='phantomjs'):
        EventsGrabber.__init__(self, verbose, browser)
        self.addresses = []

    def grab_count_of_pages(self, period):
        if period == 'future':
            url = 'http://www.2do2go.ru/msk/events'
        else:
            url = 'http://www.2do2go.ru/msk/events?end=' + datetime.now().strftime(
                '%Y-%m-%d') + '&overpast=true'

        self.driver.get(url)
        elms = self.driver.find_elements_by_css_selector('li.paginator_item')
        number_of_pages = int(elms[len(elms) - 1].text)
        return number_of_pages

    def grab_pages_with_objects(self, period='future', start_page=1, number_of_pages=0):
        if self.verbose:
            start_time_point = datetime.now()

        self.pages = []
        self.events = []

        if period == 'future':
            url_pattern = 'http://www.2do2go.ru/msk/events?page='
        else:
            url_pattern = 'http://www.2do2go.ru/msk/events?end=' + datetime.now().strftime(
                '%Y-%m-%d') + '&overpast=true&page='

        page_number = start_page
        last_page = start_page + number_of_pages
        while 1:
            if self.verbose:
                time_point = datetime.now()

            self.driver.get(url_pattern + str(page_number))

            events_links = self.driver.find_elements_by_class_name('medium-events-list_link')
            addresses = self.driver.find_elements_by_class_name('medium-events-list_address')
            self.set_pages(events_links)

            for address in addresses:
                if address.text != '':
                    self.addresses.append(address.text)
                else:
                    self.addresses.append(0)

            # log time ignores validate part
            if self.verbose:
                self.print_log(time_point, '{1:d}\ngrabbed page {2:d} in {0:d}\n{3:s}\n',
                               [len(self.pages), page_number, self.driver.current_url])

            page_number += 1

            # last page validate
            if number_of_pages != 0 and page_number == last_page:
                break
            if self.grab_value_via_try_except_by('div.paginator_next > a') == 0:
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

            info_labels = self.driver.find_elements_by_class_name('event-info_label')
            info_labeled = self.driver.find_elements_by_class_name('event-info_labeled')

            time_from = 0
            time_till = 0

            if len(self.driver.find_elements_by_class_name('event-schedule_date')) != 0:
                date = self.driver.find_element_by_class_name('event-schedule_date').text
                if len(self.driver.find_elements_by_class_name('event-schedule_start')) != 0:
                    time_from = date + ', ' + self.driver.find_element_by_class_name('event-schedule_start').text
                    time_from = self.string_to_date(time_from)
                if len(self.driver.find_elements_by_class_name('event-schedule_end')) != 0:
                    time_till = date + ', ' + self.driver.find_element_by_class_name('event-schedule_end').text
                    time_till = self.string_to_date(time_till)

            place = self.grab_value_via_try_except_by('div.event-schedule_place-name')
            categories = self.get_parallel_attribute(info_labels, info_labeled, u'Категории:').split(', ')
            categories = categories.split(', ') if isinstance(categories, str) else None

            event = dict(title=self.grab_value_via_try_except_by('h1.h__xbig').lower(),
                         subjects=categories,
                         price=self.split_prices(self.get_parallel_attribute(info_labels, info_labeled, u'Цена:')),
                         place=place.lower() if isinstance(place, basestring) else None,
                         address=self.addresses[pages.index(page)].lower(), href=page,
                         duration={'from': time_from, 'till': time_till})
            self.events.append(event)

            if self.verbose:
                self.print_log(time_point, 'grabbed page in {0:d} seconds\n{1:f}%',
                               [float((pages.index(page) + 1)) / len(pages)])

        self.save(self.events)

        if self.verbose:
            self.print_log(start_time_point, 'grabbed {1:d} pages in {0:d} seconds', [len(pages)])