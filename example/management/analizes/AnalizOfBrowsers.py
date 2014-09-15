# coding=utf-8
from example.management.analizes.Analiz import Analiz
from example.management.grabbers.events.EventsGrabber import EventsGrabber as Grabber
from datetime import datetime


class AnalizOfBrowsers(Analiz):
    def create_different_browsers(self):
        for i in range(4):
            self.grabbers.append(Grabber())
            self.times.append([])
        self.grabbers[0].set_driver('phantomjs', 0)
        self.grabbers[1].set_driver('phantomjs', options=[['--load-images=false']])
        self.grabbers[2].set_driver('firefox', 0)
        self.grabbers[3].set_driver('firefox')

        # names for plote
        self.line_names = ['phantomjs',
                           'phantomjs without image',
                           'firefox',
                           'firefox without css, image, flash']

    def complete_cycle(self):
        """ compare running time of loading/grab page and working with DOM
        """
        self.create_different_browsers()

        url_pattern = 'http://www.2do2go.ru/msk/events?end=' + datetime.now().strftime(
            '%Y-%m-%d') + '&overpast=true&page='
        limit_of_events = 1

        for i in range(len(self.grabbers)):
            page_number = 1

            # grabbed pages
            while 1:
                self.grabbers[i].driver.get(url_pattern + str(page_number))

                self.grabbers[i].pages = []
                events_links = self.grabbers[i].driver.find_elements_by_class_name('medium-events-list_link')
                self.grabbers[i].set_pages(events_links)

                page_number += 1

                if self.grabbers[i].grab_value_via_try_except_by('div.paginator_next > a') == 0 or len(
                        self.grabbers[i].pages) > limit_of_events:
                    break

            # grabbed page
            for page in self.grabbers[i].pages:
                t0 = datetime.now()
                self.grabbers[i].driver.get(url_pattern + str(page_number))

                self.grabbers[i].driver.get(page)

                info_labels = self.grabbers[i].driver.find_elements_by_class_name('event-info_label')
                info_labeled = self.grabbers[i].driver.find_elements_by_class_name('event-info_labeled')

                likes = {
                    'vk': self.grabbers[i].grab_value_via_try_except_by(
                        '//ul/li[1]/span[2]', 'xpath'),
                    'facebook': self.grabbers[i].grab_value_via_try_except_by(
                        '//ul/li[2]/span[2]', 'xpath'),
                    'ok': self.grabbers[i].grab_value_via_try_except_by(
                        '//ul/li[3]/span[2]', 'xpath'),
                    'twitter': self.grabbers[i].grab_value_via_try_except_by(
                        '//ul/li[4]/span[2]', 'xpath'),
                    'google': self.grabbers[i].grab_value_via_try_except_by(
                        '//ul/li[5]/span[2]', 'xpath'),
                    'count_of_comments': len(self.grabbers[i].driver.find_elements_by_css_selector(
                        'ul.comments-tree_branch > li')),
                    'count_of_2do2go_likes': self.grabbers[i].driver.find_element_by_class_name('btn-counter').text}

                event = {"title": self.grabbers[i].grab_value_via_try_except_by('h1.h__xbig'),
                         "subjects": self.grabbers[i].get_parallel_attribute(info_labels, info_labeled, u'Категории:'),
                         "price": self.grabbers[i].get_parallel_attribute(info_labels, info_labeled, u'Цена:'),
                         "place": self.grabbers[i].grab_value_via_try_except_by('a.event-schedule_place-link'),
                         "likes": likes,
                         "count_of_contents": len(self.grabbers[i].driver.find_elements_by_class_name('gallery_item')),
                         "href": page}
                self.grabbers[i].events.append(event)

                t1 = datetime.now()
                self.times[i].append(t1 - t0)
            self.grabbers[i].driver.close()

        self.showTimePlot()

    def incomplete_cycle(self):
        """ compare running time of loading page
        """
        self.create_different_browsers()

        url_pattern = 'http://www.2do2go.ru/msk/events?end=' + datetime.now().strftime(
            '%Y-%m-%d') + '&overpast=true&page='
        limit_of_pages = 500

        for i in range(self.grabbers.__len__()):
            page_number = 1

            while 1:
                t0 = datetime.now()
                self.grabbers[i].driver.get(url_pattern + str(page_number))

                page_number += 1

                if self.grabbers[i].grab_value_via_try_except_by('div.paginator_next > a') == 0:
                    break
                elif page_number > limit_of_pages:
                    break
                t1 = datetime.now()
                self.times[i].append(t1 - t0)
            self.grabbers[i].driver.close()
        self.showTimePlot()