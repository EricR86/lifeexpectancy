from django.db import models
from django.contrib import admin

# Create your models here.
#class LifeExpectancy(models.Model):
#    country_code = models.CharField(max_length=3)
#    year_born = models.IntegerField()
#    years_expected = models.FloatField()
#
#    def __unicode__(self):
#        string = self.country_code + ", " + str(self.year_born) + ", " + str(self.years_expected)
#        return string


class LifeTableEntry(models.Model):
    country = models.CharField(max_length=64)
    year_updated = models.IntegerField()
    is_male = models.BooleanField() #assumes otherwise female

    age = models.IntegerField()
    probability_of_death_before_next_birthday = models.FloatField()
    remaining_years_left = models.FloatField()

    def __unicode__(self):

        gender_string = "F"
        if self.is_male:
            gender_string = "M"

        string = self.country + ", " + str(self.year_updated) + ", " + gender_string + ", " + str(self.remaining_years_left)
        return string

class LifeTableEntryAdmin(admin.ModelAdmin):
    list_display = ('country', 'year_updated', 'is_male', 'age')
    list_filter = ('country', 'is_male', 'year_updated')

#admin.site.register(LifeExpectancy)
admin.site.register(LifeTableEntry, LifeTableEntryAdmin)
