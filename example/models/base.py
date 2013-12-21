# -*- coding: utf-8 -*-
from django.core.exceptions import MultipleObjectsReturned
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class SeparatedValuesField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', '|||')
        super(SeparatedValuesField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value: return
        if isinstance(value, list):
            return value
        return value.split(self.token)

    def get_db_prep_value(self, value, connection, prepared=False):
        if not value: return
        assert(isinstance(value, list) or isinstance(value, tuple))
        return self.token.join([unicode(s) for s in value])

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)


class Base(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, unique=True)

    class Meta:
        abstract = True
        app_label = 'example'

    def save(self, *args, **kwargs):
        super(Base, self).save(*args, **kwargs)
        return self


class Venue(Base):
    address = models.CharField(max_length=250, null=True, blank=True)
    geo = models.ForeignKey('Point', null=True, blank=True, unique=True)
    synonyms = SeparatedValuesField(null=True, blank=True)

    def list_of_synonyms(self):
        return [{self.synonyms.index(synonym): synonym} for synonym in self.synonyms]

    def __str__(self):
        return '%s' % self.name


class Point(models.Model):
    x = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(90)])
    y = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(90)])

    class Meta:
        app_label = 'example'

    def save(self, *args, **kwargs):
        super(Point, self).save(*args, **kwargs)
        return self

    def __str__(self):
        return '[%f, %f]' % (self.x, self.y)


class DateTime(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField()

    class Meta:
        app_label = 'example'

    def save(self, *args, **kwargs):
        super(DateTime, self).save(*args, **kwargs)
        return self

    def __str__(self):
        return '%s' % self.date