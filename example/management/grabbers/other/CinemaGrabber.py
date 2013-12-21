# -*- coding: utf-8 -*-
from types import NoneType
from datetime import datetime
from example.management.grabbers.Grabber import *
from selenium.common.exceptions import ErrorInResponseException, ImeActivationFailedException
from example.models.cinema import *


class CinemaGrabber(Grabber):
    def __init__(self, verbose=0, browser='phantomjs'):
        Grabber.__init__(self, verbose, browser)
        self.cinemas = []

    def grab_cinema(self, page_number):
        self.driver.get('http://www.google.ru/movies?near=moscow,+mow,+rus&start=' + str(10 * page_number))

        output = self.driver.find_elements_by_css_selector('h2.name > a')
        pages = []
        for href in output:
            pages.append(href.get_attribute('href'))
        for page in pages:
            self.driver.get(page)

            dd = self.driver.find_element_by_css_selector('#left_nav > div.section')
            output = dd.find_elements_by_css_selector('div > a')
            films = {}

            periods = []
            for period in output:
                periods.append(period.get_attribute('href'))
            for period in periods:

                movies = self.driver.find_elements_by_class_name('movie')

                for movie in movies:

                    key = self.translit(movie.find_element_by_css_selector('div.name > a').text)
                    try:
                        films[key]
                    except KeyError:
                        films[key] = {'schedule': []}
                        films[key]['name'] = movie.find_element_by_css_selector('div.name > a').text.lower()
                        info = movie.find_element_by_css_selector('span.info').text.split(' - ')
                        for bit in info:
                            if bit.find(u'мин.') != -1:
                                bit = re.sub(u'\u200e', '', bit)
                                duration = bit.split(' ')
                                films[key]['duration'] = int(duration[0].replace(u'ч.', '')) * 60 + int(
                                    duration[1].replace(u'мин.', '')) if len(duration) == 2 else duration[0].replace(u'мин.','')
                            else:
                                films[key]['genre'] = [genre.replace(u'\u200e', '').lower() for genre in bit.split('/')]

                    times = movie.find_elements_by_css_selector('div.times > span')

                    for tu in times:
                        string = tu.text.replace(u'\u200e', '')
                        t = string.split(':')
                        year = datetime.datetime.now().year
                        month = datetime.datetime.now().month

                        # check night session
                        if t[0] < 2:
                            day = datetime.datetime.now().day + 1
                        else:
                            day = datetime.datetime.now().day

                        films[key]['schedule'].append(
                            datetime.datetime(year, month, day, int(t[0]), int(t[1])) + datetime.timedelta(
                                days=periods.index(period)))

                self.driver.get(period)

            cinema = {'films': [], 'name': self.driver.find_element_by_css_selector('h2.name').text.lower(),
                      'address': self.driver.find_element_by_css_selector('div.info').text.split(' - ')[0],
                      'href': page}

            for value in films.values():
                cinema['films'].append(value)

            self.cinemas.append(cinema)

        self.save()

    def save(self):
        Cinema.clean()
        Film.clean()

        for cinema in self.cinemas:
            try:
                try:
                    oneCinema = Cinema.objects.get(name=cinema['name'])
                except Cinema.DoesNotExist:
                    oneCinema = Cinema(name=cinema['name'])
                    geo = self.get_point(address=cinema['address'])
                    if geo is not None:
                        geo = self.get_or_create(Point, **geo)
                        try:
                            place = Venue.objects.get(geo=geo)
                        except Venue.DoesNotExist:
                            place = Venue(geo=geo, name=cinema['name'], address=cinema['address'])
                        if type(place.synonyms) is NoneType:
                            place.synonyms = [cinema['name']]
                        elif cinema['name'] not in place.synonyms:
                            place.synonyms.append(cinema['name'])
                        place.href = cinema['href']
                        place.save()
                        oneCinema.place = place

                for film in cinema['films']:

                    oneFilm = self.get_or_create(Film, name=film['name'])

                    if 'duration' in film:
                        oneFilm.duration = film['duration']

                    if 'genre' in film:
                        for genre in film['genre']:
                            oneGenre = self.get_or_create(Genre, name=genre)
                            oneFilm.genres.add(oneGenre)

                    oneFilm.save()

                    oneSchedule = Schedule(film=oneFilm)
                    oneSchedule.save()  # many-to-many relations

                    for time in film['schedule']:
                        oneDateTime = self.get_or_create(DateTime, date=time)
                        oneSchedule.schedule.add(oneDateTime)

                    oneSchedule.save()
                    oneCinema.save()  # many-to-many relations
                    oneCinema.films.add(oneSchedule)
                    oneCinema.save()
            except:
                    continue

    def grab_count_of_pages(self, period):
        if period == 'future':
            self.driver.get('http://www.google.ru/movies')
            return int(self.driver.find_elements_by_css_selector('td > a')[-2].text)

    def translit(self, locallangstring):
        conversion = {
            u'\u0410': 'A', u'\u0430': 'a',
            u'\u0411': 'B', u'\u0431': 'b',
            u'\u0412': 'V', u'\u0432': 'v',
            u'\u0413': 'G', u'\u0433': 'g',
            u'\u0414': 'D', u'\u0434': 'd',
            u'\u0415': 'E', u'\u0435': 'e',
            u'\u0401': 'Yo', u'\u0451': 'yo',
            u'\u0416': 'Zh', u'\u0436': 'zh',
            u'\u0417': 'Z', u'\u0437': 'z',
            u'\u0418': 'I', u'\u0438': 'i',
            u'\u0419': 'Y', u'\u0439': 'y',
            u'\u041a': 'K', u'\u043a': 'k',
            u'\u041b': 'L', u'\u043b': 'l',
            u'\u041c': 'M', u'\u043c': 'm',
            u'\u041d': 'N', u'\u043d': 'n',
            u'\u041e': 'O', u'\u043e': 'o',
            u'\u041f': 'P', u'\u043f': 'p',
            u'\u0420': 'R', u'\u0440': 'r',
            u'\u0421': 'S', u'\u0441': 's',
            u'\u0422': 'T', u'\u0442': 't',
            u'\u0423': 'U', u'\u0443': 'u',
            u'\u0424': 'F', u'\u0444': 'f',
            u'\u0425': 'H', u'\u0445': 'h',
            u'\u0426': 'Ts', u'\u0446': 'ts',
            u'\u0427': 'Ch', u'\u0447': 'ch',
            u'\u0428': 'Sh', u'\u0448': 'sh',
            u'\u0429': 'Sch', u'\u0449': 'sch',
            u'\u042a': '"', u'\u044a': '"',
            u'\u042b': 'Y', u'\u044b': 'y',
            u'\u042c': '\'', u'\u044c': '\'',
            u'\u042d': 'E', u'\u044d': 'e',
            u'\u042e': 'Yu', u'\u044e': 'yu',
            u'\u042f': 'Ya', u'\u044f': 'ya',
        }
        translitstring = []
        for c in locallangstring:
            translitstring.append(conversion.setdefault(c, c))
        return ''.join(translitstring)

    def start(self, queue, grabber, browser_name):
        while True:
            job = queue.get()

            if job is None:
                break

            while 1:
                try:
                    a = datetime.now()
                    grabber.__init__(0, browser_name)
                    grabber.grab_cinema(job[0])
                    queue.task_done()
                    print '+ %d %d' % (len(grabber.cinemas), datetime.now() - a)
                    break
                except (ErrorInResponseException, ImeActivationFailedException, KeyboardInterrupt):
                    print "4_Unexpected error: %s url: %s" % (sys.exc_info()[0], grabber.driver.current_url)
                    grabber.driver.quit()
                    exit(0)
        queue.task_done()