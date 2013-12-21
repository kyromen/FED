from example.models.base import *


class Cinema(Base):
    place = models.ForeignKey('Venue', null=True, blank=True)
    films = models.ManyToManyField('Schedule')
    price_min = models.PositiveIntegerField(null=True, blank=True)
    price_max = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return '%s' % self.name


class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    film = models.ForeignKey('Film', db_index=True)
    schedule = models.ManyToManyField('DateTime')

    class Meta:
        app_label = 'example'

    def save(self, *args, **kwargs):
        super(Schedule, self).save(*args, **kwargs)
        return self

    def __str__(self):
        return '%s' % self.film.name


class Film(Base):
    duration = models.IntegerField(null=True, blank=True)
    genres = models.ManyToManyField('Genre', null=True, blank=True)

    def __str__(self):
        return '%s' % self.name


class Genre(Base):
    def __str__(self):
        return '%s' % self.name