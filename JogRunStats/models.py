# -*- coding: utf8 -*-
from django.db import models
import datetime
# Create your models here.

STOP_CAUSES = (
  (1, 'Pee'),
  (2, 'Little Rest'),
  (3, 'Medium Rest'),
  (4, 'Long Rest'),
  (5, 'Phone call'),
  (6, 'Battery replacing'),
  (7, 'Moving something somewhere'),
)
RAIN_TYPES = (
  (1, 'No rain after rain or intermittent light rain'),
  (2, 'Light rain'),
  (3, 'Windy Light rain'),
  (4, 'Normal Cold rain'),
  (5, 'Normal Warm rain'),
  (6, 'Pouring Warm rain'),
  (7, 'Pouring Cold rain'),
)

PLACES = (
  (1, 'Carmela Dutra Home'),
  (1, 'Heitor Beltrão, Carmela Dutra Bus Stop'),
  (2, 'Light rain'),
          
)

class Daytimes(models.Model):
  atPlace = models.IntegerField(choices=)

class JogRunStat(models.Model):
  date    = models.DateField(default=datetime.date.today())
  runtime = models.TimeField(default=0)
  cost    = models.DecimalField(default=0.0)
  stops   = models.ManyToManyRel(choices=STOP_CAUSES)
  ifRainWhatKind = models.ManyToManyRel(choices=STOP_CAUSES)
  temperature = models.DecimalField(default=0.0)
  isBikeless = models.BooleanField(default=True)
  daytimes = models.ManyToManyField()
