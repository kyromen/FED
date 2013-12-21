# -*- coding: utf-8 -*-
from EventsGrabber import *


class LookAtMeGrabber(EventsGrabber):
    def __init__(self, verbose=0, browser='phantomjs'):
        EventsGrabber.__init__(self, verbose, browser)
        self.addresses = []

    def grab_count_of_pages(self, period='future'):
        if period == 'future':
            url = 'http://www.lookatme.ru/cities/moscow/events/'
        else:
            return (datetime.now().year - 2007) * 356
        self.driver.get(url)
        pages = self.driver.find_elements_by_css_selector('ul.pages > li > a')
        number_of_pages = int(pages[len(pages) - 1].text)
        return number_of_pages

    def grab_pages_with_objects(self, period='future', start_page=0, number_of_pages=0):
        if self.verbose:
            start_time_point = datetime.now()
            page_number = 1

        self.pages = []
        self.events = []

        if period == 'future':
            url_pattern = 'http://www.lookatme.ru/cities/moscow/events?&page='
            page_generator = lambda ptrn, number: ptrn + str(number)
        else:
            url_pattern = 'http://www.lookatme.ru/cities/moscow/events/'
            page_generator = lambda ptrn, number: ptrn + (
                datetime.now() - datetime.timedelta(days=number)).strftime(
                    '%Y-%m-%d')

        current_day = start_page
        last_day = start_page + number_of_pages

        while 1:
            if self.verbose:
                time_point = datetime.now()

            self.driver.get(page_generator(url_pattern, current_day))
            current_day += 1
            page_internal_number = 1

            while 1:
                if self.verbose:
                    time_point_internal = datetime.now()

                events_links = self.driver.find_elements_by_css_selector('div.title > a')
                self.set_pages(events_links)

                # log time ignores validate part
                if self.verbose:
                    if self.verbose:
                        self.print_log(time_point_internal, '{2:d}\ngrabbed page {1:d} in: {0:d}',
                                       [page_internal_number, len(self.pages)])
                        page_number += 1

                if period == 'future':
                    break

                # last page validate
                if len(self.driver.find_elements_by_css_selector('a.arrow-next')) != 0:
                    self.driver.find_element_by_css_selector('a.arrow-next').click()
                else:
                    break

            # log time ignores validate part
            if number_of_pages != 0 and current_day == last_day:
                break
            if self.verbose:
                self.print_log(time_point, '{1:d}\ngrabbed day in {0:d}\n{2:s}\n',
                               [len(self.pages), self.driver.current_url])

        if self.verbose:
            self.print_log(start_time_point, 'grabbed {1:d} days/{2:d} pages in {0:d} seconds\n',
                           [current_day - start_page, page_number])

    def grab_events_pages(self, pages=None):
        if self.verbose:
            start_time_point = datetime.now()

        if pages is None:
            pages = self.pages

        for page in pages:
            try:
                if self.verbose:
                    time_point = datetime.now()
                    self.driver.get(page)
                    print '%s\npage loading time: %d' % (page, (datetime.now() - time_point).seconds)
                else:
                    self.driver.get(page)

                if u'ошибка 500' in self.driver.title:
                    print "Error 500"
                    continue

                info_dts = self.driver.find_elements_by_css_selector('dl.info > dt')
                info_dds = self.driver.find_elements_by_css_selector('dl.info > dd')

                if len(self.driver.find_elements_by_class_name('date')):
                    date = self.driver.find_element_by_class_name('date').text
                    date += ' ' + self.driver.find_element_by_class_name('month').text
                    date += ', ' + self.get_parallel_attribute(info_dts, info_dds, u'НАЧАЛО')
                    duration = self.string_to_date(date)

                event = dict(title=self.grab_value_via_try_except_by('h1.b-article-title').lower(),
                             subjects=self.grab_value_via_try_except_by('div.g-line-center-block > ins').lower(),
                             price=self.split_prices(self.get_parallel_attribute(info_dts, info_dds, u'ЦЕНА')),
                             place=self.grab_value_via_try_except_by('h2.b-article-flow > a').lower(),
                             address=self.get_parallel_attribute(info_dts, info_dds, u'АДРЕС').lower(), href=page,
                             duration={'from': duration, 'till': 0})
                self.events.append(event)

                if self.verbose:
                    self.print_log(time_point, 'grabbed page in {0:d} seconds\n{1:f}%',
                                   [float((pages.index(page) + 1)) / len(pages) * 100])
            except WebDriverException:
                continue
        self.save(self.events)

        if self.verbose:
            self.print_log(start_time_point, 'grabbed {1:d} pages in {0:d} seconds', [len(self.pages)])