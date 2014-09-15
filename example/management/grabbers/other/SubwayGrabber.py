# -*- coding: utf-8 -*-
from example.management.grabbers.Grabber import *
from example.models.district import Subway, Point, Line


class SubwayGrabber(Grabber):
    def __init__(self, verbose=0, browser='phantomjs'):
        Grabber.__init__(self, verbose, browser)
        self.subways = []

    def grab_stations_info(self):
        self.driver.get(
            'http://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%81%D1%82%D0%B0%D0%BD%D1%86%D0%B8%D0%'
            'B9_%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%B3%D0%BE_%D0%BC%D0%B5%D1%82%D1%80%D0%BE%D0%BF'
            '%D0%BE%D0%BB%D0%B8%D1%82%D0%B5%D0%BD%D0%B0')

        trs = self.driver.find_elements_by_css_selector('table.sortable > tbody > tr')

        for tr in trs:
            subway = {
                'name': tr.find_elements_by_css_selector('td > span > a')[1].text.lower(),
                'line': [
                    self.get_number_line(tr.find_element_by_css_selector('.sortkey').get_attribute('innerHTML')),
                    tr.find_elements_by_css_selector('td > span')[1].get_attribute('title').lower()
                ],
                'geo': self.get_geo(tr.find_element_by_css_selector('span.geo-dec span.vcard span.geo-dec').text)
            }
            self.subways.append(subway)

        self.save(self.subways)
        self.driver.quit()

    @staticmethod
    def get_geo(text):
        geo = re.findall("\d+\.\d+", text)
        return [float(i) for i in geo]

    @staticmethod
    def get_number_line(text):
        if text[0] == '0':
            text = text[1:]
        return int(text)

    def save(self, subways):
        for subway in subways:
            point = Point.objects.get_or_create(x=subway['geo'][0], y=subway['geo'][1])[0]
            line = Line.objects.get_or_create(name=subway['line'][1], line_number=subway['line'][0])[0]

            try:
                sbw = Subway.objects.get(name=subway['name'])
            except Subway.DoesNotExist:
                sbw = Subway(name=subway['name'])
                sbw.geo = point
                sbw.save()

            sbw.lines.add(line)
            sbw.save()