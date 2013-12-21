from example.models.base import *


class District(Base):
    region = models.ManyToManyField('Region', related_name='region')

    def __str__(self):
        return '%s' % self.name


class Region(Base):
    subways = models.ManyToManyField('Subway', null=True, blank=True)

    def __str__(self):
        return '%s' % self.name


class Subway(Base):
    geo = models.OneToOneField('Point')
    lines = models.ManyToManyField('Line')

    def __str__(self):
        return '%s' % self.name


class Line(Base):
    line_number = models.SmallIntegerField()

    def __str__(self):
        return '%s' % self.name