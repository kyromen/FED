from django.contrib import admin
from example.autocompete import AutocompleteModelAdmin
from example.models.district import *
from example.models.event import *
from example.models.cinema import *


class DefaultAdmin(admin.ModelAdmin):
    pass


class BaseAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ('name',)


class FilmAdmin(AutocompleteModelAdmin):
    related_search_fields = dict(genre=('name',))
    search_fields = ['name']


class DistrictAdmin(AutocompleteModelAdmin):
    related_search_fields = dict(region=('name',))


admin.site.register(Event, BaseAdmin)
admin.site.register(Subject, BaseAdmin)
admin.site.register(Venue, BaseAdmin)

admin.site.register(Cinema, BaseAdmin)
admin.site.register(Film, FilmAdmin)
admin.site.register(Genre, BaseAdmin)
admin.site.register(Schedule, DefaultAdmin)

admin.site.register(DateTime, DefaultAdmin)
admin.site.register(Point, DefaultAdmin)

admin.site.register(District, DistrictAdmin)
admin.site.register(Region, BaseAdmin)
admin.site.register(Subway, BaseAdmin)