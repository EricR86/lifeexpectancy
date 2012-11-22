from django.db import models
from django.contrib import admin

# Create your models here.
class LifeExpectancy(models.Model):
    country_code = models.CharField(max_length=3)
    year_born = models.IntegerField()
    years_expected = models.FloatField()

    def __unicode__(self):
        string = self.country_code + ", " + str(self.year_born) + ", " + str(self.years_expected)
        return string

admin.site.register(LifeExpectancy)
