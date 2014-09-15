# -*- coding: utf-8 -*-
from __future__ import with_statement
import signal
from contextlib import contextmanager
from types import NoneType
from urllib2 import URLError
from httplib import BadStatusLine
from django.db import IntegrityError

from selenium.common.exceptions import \
    ErrorInResponseException, \
    WebDriverException, \
    ImeActivationFailedException, \
    NoSuchElementException

from example.models.event import *
from example.models.district import Subway
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


class EventsGrabber(Grabber):
    def __init__(self, verbose=0, browser='phantomjs'):
        Grabber.__init__(self, verbose, browser)
        self.events = []

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
                            # limit of initialize browser running time
                            with time_limit(15):
                                grabber = grabber_cls(0, browser_name)
                                start = False

                        # limit of grabber running time
                        with time_limit(1800):
                            grabber.grab_pages_with_objects('future', job[0], job[1])
                            grabber.grab_events_pages()
                            queue.task_done()
                            break
                    except TimeoutException:
                        print "Error:", sys.exc_info()[0]
                        grabber.driver.quit()
                    except (ErrorInResponseException, ImeActivationFailedException, KeyboardInterrupt):
                        print "Error: %s url: %s" % (sys.exc_info()[0], grabber.driver.current_url)
                        grabber.driver.quit()
                        exit(0)
                    except (BadStatusLine, URLError):
                        print "Error:", sys.exc_info()[0]
                        grabber = grabber_cls(0, browser_name)
                        continue
                except (WebDriverException, URLError, BadStatusLine):
                    grabber = grabber_cls(0, browser_name)
        grabber.driver.quit()
        queue.task_done()

    def set_pages(self, pages):
        for page in pages:
            href = page.get_attribute('href')
            try:
                Event.objects.get(href=href)
            except Event.DoesNotExist:
                self.pages.append(href)

    def grab_value_via_try_except_by(self, selector, by='css'):
        try:
            if by == 'xpath':
                value = self.driver.find_element_by_xpath(selector).text
            else:
                value = self.driver.find_element_by_css_selector(selector).text
            if value == '+1':  # vk like
                value = 0
            elif value == '' or value == ' ':
                value = -2
        except NoSuchElementException:
            value = -3
        return value

    def split_prices(self, price):
        try:
            prices = re.findall("([\d]{2,})", price)
            return_price = {'from': int(prices[0]), 'till': int(prices[0])}
            for price in prices:
                price = int(price)
                if return_price['from'] > price:
                    return_price['from'] = price
                elif return_price['till'] < price:
                    return_price['till'] = price
            return return_price
        except (IndexError, TypeError):
            return {'none': 1}

    def string_to_date(self, string):
        months = {
            u'янв': 1,
            u'фев': 2,
            u'мар': 3,
            u'апр': 4,
            u'мая': 5,
            u'июн': 6,
            u'июл': 7,
            u'авг': 8,
            u'сен': 9,
            u'окт': 10,
            u'ноя': 11,
            u'дек': 12
        }

        parts = string.split(', ')
        day_and_month = parts[0].split(' ')

        day_and_month[1] = months[day_and_month[1][:3]]
        hour_and_min = parts[1].split(':')

        max_duration = 6

        if max_duration < day_and_month[1] >= abs((13 + datetime.now().month - max_duration) % 12):
            year = datetime.now().year
        elif max_duration > day_and_month[1] >= abs((13 + datetime.now().month - max_duration) % 12):
            year = datetime.now().year - 1
        else:
            year = datetime.now().year + 1

        if hour_and_min[0] == u'Круглосуточно':
            return datetime(year, day_and_month[1], int(day_and_month[0]))

        return datetime(year, day_and_month[1], int(day_and_month[0]), int(hour_and_min[0]),
                                 int(hour_and_min[1]))

    def get_nearest_subways(self, point):
        subways = Subway.objects.filter(geo__x__gt=point.x - 0.01, geo__x__lt=point.x + 0.01,
                                        geo__y__gt=point.y - 0.01, geo__y__lt=point.y + 0.01)
        return subways

    def save(self, events):
        for one_event in events:
            try:
                try:
                    event = Event.objects.get(name=one_event['title'])
                except Event.DoesNotExist:
                    event = Event(name=one_event['title'], href=one_event['href'])
                    if 'price' in one_event:
                        if 'none' not in one_event['price']:
                            if one_event['price']['from'] != one_event['price']['till']:
                                event.price_max = one_event['price']['till']
                            event.price_min = one_event['price']['from']
                    if 'duration' in one_event:
                        if one_event['duration']['from'] != 0:
                            event.start = one_event['duration']['from']
                        if one_event['duration']['till'] != 0:
                            event.end = one_event['duration']['till']

                    event.save()

                if isinstance(one_event['address'], basestring):
                    geo = self.get_point(one_event['address'])
                    if geo:
                        geo = self.get_or_create(Point, **geo)
                        try:
                            place = Venue.objects.get(geo=geo)
                        except Venue.DoesNotExist:
                            try:
                                place = Venue.objects.get(name=one_event['place'])
                                place.geo = geo
                                place.address = one_event['address']
                            except Venue.DoesNotExist:
                                place = Venue(geo=geo, name=one_event['place'], address=one_event['address'])
                        except MultipleObjectsReturned:
                            place = Venue.objects.filter(geo=geo)[0]
                    else:
                        place = self.get_or_create(Venue, name=one_event['place'])
                    if type(place.synonyms) is NoneType:
                        place.synonyms = [one_event['place']]
                    elif one_event['place'] not in place.synonyms:
                        place.synonyms.append(one_event['place'])

                    place.save()
                    event.place = place

                if isinstance(one_event['subjects'], basestring):
                    subject = self.get_or_create(Subject, name=one_event['subjects'])
                    event.subjects.add(subject)
                elif isinstance(one_event['subjects'], list):
                    for sbjct in one_event['subjects']:
                        subject = self.get_or_create(Subject, name=sbjct)
                        event.subjects.add(subject)

                event.save()
            except IntegrityError:
                continue