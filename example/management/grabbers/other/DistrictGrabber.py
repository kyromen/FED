# -*- coding: utf-8 -*-
from example.management.grabbers.Grabber import *
from example.models.district import District, Region, Subway


class DistrictGrabber(Grabber):
    def __init__(self, verbose=0, browser='phantomjs'):
        Grabber.__init__(self, verbose, browser)
        self.districts = []

    def grab_districts_info(self):
        self.driver.get(
            'http://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%80%D0%B0%D0%B9%D0%BE%D0%BD%D0%BE%D0%'
            'B2_%D0%B8_%D0%BC%D1%83%D0%BD%D0%B8%D1%86%D0%B8%D0%BF%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85_%D0%BE%D0%B1%D1%8'
            '0%D0%B0%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B9_%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D1%8B')

        trs = self.driver.find_elements_by_css_selector('table.sortable > tbody > tr')
        hrefs = []

        for tr in trs[1:]:
            hrefs.append(tr.find_elements_by_css_selector('td > a')[0].get_attribute('href'))

        for href in hrefs:
            self.driver.get(href)

            ths = self.driver.find_elements_by_css_selector('table.infobox > tbody > tr > th')[:-3]
            tds = self.driver.find_elements_by_css_selector('table.infobox > tbody > tr > td > p')[1:-1]

            self.clean_array(u'^\s+|Район|Муниципальный округ|Характеристика|\s+$', ths)
            subways = self.get_parallel_attribute(ths, tds, u'Станции метро')
            if subways != 0:
                subways = subways.split(', ')
                if len(subways) == 1:
                    subways = subways[0].split('\n')
                if len(subways) == 1:
                    subways = subways[0].split(u' и ')
                for i in range(len(subways)):
                    subways[i] = re.sub(u"^\s+| \([а-яА-Яa-zA-Z0-9]*\)|«|»|-кольцевая|\.|\s+$", '', subways[i])
            region_name = self.get_parallel_attribute(ths, tds, u'Название района')
            if region_name == 0:
                region_name = self.get_parallel_attribute(ths, tds, u'Название')
            district_name = self.get_parallel_attribute(ths, tds, u'Административный округ')
            if len(district_name) > 6:
                district_name = ''.join(word[0] for word in re.sub('-', ' ', district_name).split(' '))
            if district_name == u'южный':
                district_name = u'юао   '
            district = dict(region_name=region_name, district_name=district_name, subways=subways)
            self.districts.append(district)

        self.save(self.districts)

    def save(self, districts):
        for one_district in districts:
            region = self.get_or_create(Region, name=one_district['region_name'])

            if one_district['subways']:
                for subway in one_district['subways']:
                    try:
                        subway = Subway.objects.get(name=subway)
                        region.subways.add(subway)
                    except ObjectDoesNotExist:
                        print subway
                region.save()

            district = self.get_or_create(District, name=one_district['district_name'])
            district.region.add(region)
            district.save()