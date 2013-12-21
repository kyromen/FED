# -*- coding: utf-8 -*-
import re
from datetime import datetime

from django.http import HttpResponse
from pymorphy.contrib import tokenizers
from django.template import loader, RequestContext

from example.models.cinema import *
from example.models.event import *
from example.models.district import *

from pymorphy.django_conf import default_morph as morph


def home(request):
    if request.method == 'GET' and 'search' in request.GET:
        district = ''
        regions = []
        subways = []

        films = []
        genres = []

        subjects = []

        day = datetime.now()

        string = request.GET['search']
        strings = re.split(u'[\.]+|!|\?', string)
        words = []

        for string in strings:
            for word in tokenizers.extract_words(string):
                words.append(word.upper())
        for word in words:
            word = word.upper()
            info = morph.get_graminfo(word)

            if info[0]['class'] == 'С':
                if check_object(District, {'name': word.lower()}):
                    district = word.lower()
                if check_object(Region, {'name__regex': r'(^' + info[0]['norm'].lower() + ')'}) and len(
                        words) > words.index(word) + 1:
                    if search_by_touch(Region, info[0]['norm'], words[words.index(word) + 1]):
                        regions.append(search_by_touch(Region, info[0]['norm'], words[words.index(word) + 1]))
                elif check_object(Region, {'name__regex': r'(^' + info[0]['norm'].lower() + '$)'}):
                    regions.append(word.lower())
                if check_object(Subway, {'name__regex': r'(^' + word.lower() + ' )'}) and len(words) > words.index(
                        word) + 1:
                    query_str = word
                    for word_ in words[words.index(word) + 1:words.index(word) + 2]:
                        if check_object(Subway, {'name__regex': r'(^' + query_str.lower() + '$)'}):
                            subways.append(Subway.objects.get(name=query_str.lower()))
                            break
                        query_str += ' ' + word_
                elif check_object(Subway, {'name__regex': r'(^' + word.lower() + '$)'}):
                    subways.append(Subway.objects.get(name=word.lower()))
                if check_object(Subject, {'name': info[0]['norm'].lower()}):
                    subjects.append(Subject.objects.get(name=info[0]['norm'].lower()))
                if check_object(Genre, {'name': info[0]['norm'].lower()}):
                    genres.append(Genre.objects.get(name=info[0]['norm'].lower()))
            elif info[0]['class'] == 'П':
                if len(words) > words.index(word) + 1:
                    if search_by_touch(Region, word, words[words.index(word) + 1]):
                        regions.append(search_by_touch(Region, word, words[words.index(word) + 1]))
                    if check_object(Subway, {'name__regex': r'(^' + word.lower() + ' )'}) and len(
                            words) > words.index(word) + 1:
                        query_str = word
                        for word_ in words[words.index(word) + 1:words.index(word) + 3]:
                            if check_object(Subway, {'name__regex': r'(^' + query_str.lower() + '$)'}):
                                subways.append(Subway.objects.get(name=query_str.lower()))
                                break
                            query_str += ' ' + word_
                elif check_object(Region, {'name__regex': r'(^' + info[0]['norm'].lower() + '$)'}):
                    regions.append(word.lower())
                elif check_object(Subway, {'name__regex': r'(^' + word.lower() + '$)'}):
                    subways.append(Subway.objects.get(name=word.lower()))
            elif info[0]['class'] == 'Н':
                time = re.search('\d{2}:\d{2}', string)
                if time:
                    time = time.group(0)
                    if word == u'завтра':
                        day = datetime.datetime(day.year, day.month, day.day + 1, int(time.split(':')[0]),
                                                int(time.split(':')[1]))
                    else:
                        day = datetime.datetime(day.year, day.month, day.day, int(time.split(':')[0]),
                                                int(time.split(':')[1]))
                elif word == u'завтра':
                    day = day + datetime.timedelta(days=1)

        events = []
        cinemas = []

        for film in Film.objects.filter(genres__in=genres):
            films.append(film.name)

        if district != '':
            district = District.objects.get(name=district)
            for region in district.region.all():
                regions.append(region.name)
        for name in regions:
            region = Region.objects.get(name=name)
            for subway in region.subways.all():
                subways.append(subway)

        for subway in subways:
            filter_parameters = {'place__geo__x__gt': subway.geo.x - 0.005,
                                 'place__geo__x__lt': subway.geo.x + 0.005,
                                 'place__geo__y__gt': subway.geo.y - 0.005,
                                 'place__geo__y__lt': subway.geo.y + 0.005}

            output = Event.objects.filter(**filter_parameters)
            for event in output:
                events.append(event)

            if films:
                filter_parameters['films__film__name__in'] = films

            output = Cinema.objects.filter(**filter_parameters)
            for cinema in output:
                if cinema not in cinemas:
                    cinemas.append(cinema)

        if cinemas.__len__() == 0:
            output = Cinema.objects.filter(films__film__name__in=films)
            for cinema in output:
                if cinema not in cinemas:
                    cinemas.append(cinema)

        if events and subjects:
            output = events
            events = []
            for i in range(output.__len__() - 1, -1, -1):
                for subject in output[i].subjects.all():
                    if subject in subjects:
                        events.append(output[i])
                        break
        elif subjects:
            for event in Event.objects.filter(subjects__in=subjects):
                events.append(event)

        places = []
        for i in range(events.__len__() - 1, -1, -1):
            if events[i].place not in places:
                places.append(events[i].place)
            else:
                events.pop(i)

        t = loader.get_template('home.html')
        c = RequestContext(request, {'events': events, 'cinemas': cinemas})
        return HttpResponse(t.render(c))

    t = loader.get_template('home.html')
    c = RequestContext(request, {'objects': {}})
    return HttpResponse(t.render(c))


def check_object(object, parameters):
    try:
        object.objects.get(**parameters)
    except object.DoesNotExist:
        return 0
    except MultipleObjectsReturned:
        None
    return 1


def search_by_touch(object, adj, noun):
    info = morph.get_graminfo(noun.upper())
    for inf in info:
        adj_ = morph.inflect_ru(adj.upper(), inf['info'])
        for i in range(2):
            for j in range(2):
                string = (noun * i + ' ' * i * j + adj_ * j).lower()
                if check_object(object, {'name__regex': r'(^' + string + '$)'}):
                    return string
                string = (adj * (1 - j) + adj_ * i * j + ' ' * i * j + noun * j).lower()
                if check_object(object, {'name__regex': r'(^' + string + '$)'}):
                    return string
    return 0