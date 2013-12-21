from example.models.base import *


class Event(Base):
    subjects = models.ManyToManyField('Subject', null=True, blank=True)
    place = models.ForeignKey('Venue', null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    price_min = models.PositiveIntegerField(null=True, blank=True)
    price_max = models.PositiveIntegerField(null=True, blank=True)
    href = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return '%s' % self.name


class Subject(Base):
    def __str__(self):
        return '%s' % self.name



