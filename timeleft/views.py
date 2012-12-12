from django.template import RequestContext
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.core import serializers

#from models import LifeExpectancy
from models import LifeTableEntry

import json
import urllib2
from datetime import date, timedelta

def main(request):
    context_dict = {}

    return render_to_response('main.html',
                              context_dict,
                              context_instance=RequestContext(request))


def show_results(request, country, gender, birth_year, birth_month, birth_day):
    context_dict = {}

    # Calculate the age given the birthday
    age = 0
    birthday = date(int(birth_year), int(birth_month), int(birth_day))
    # First calc the difference in years
    today = date.today()
    age = today.year - birthday.year
    # If today's current month and day is before the birthday, subtract 1 from
    # the age (we haven't hit this year's birthday)
    if today.month <= birthday.month and today.day < birthday.day:
        age -= 1

    gender = gender.capitalize()
    country = country.capitalize()

    # Lookup the projected life left based on country, gender, and age
    results = LifeTableEntry.objects.filter(
            country = country,
            is_male = (gender == 'M'),
            age = age,
    )

    if results.exists() == False:
        raise Http404

    life_data = results[0]

    # Calculate the est date of death from years remaining past the birthday
    # Get years remaining and covert into days remaining
    years_remaining = life_data.remaining_years_left
    days_remaining = int(round(years_remaining * 365.242199))
    # Add to birthday
    die_date = birthday + timedelta(days=days_remaining)
    #life_data.probability_of_death_before_next_birthday *= 100.0

    # Display results 
    context_dict['life_data'] = life_data
    context_dict['percentage_life_left'] = sig_digits(
        life_data.remaining_years_left / (age + life_data.remaining_years_left), 
        3
    )
    context_dict['days_remaining'] = days_remaining
    context_dict['die_date'] = die_date
    # (probability, remaining years left, rough days left,  rough est date of death)
    return render_to_response('results.html',
                              context_dict,
                              context_instance=RequestContext(request))

def sig_digits(x, n):
    if n < 1:
        raise ValueError("number of significant digits must be >= 1")
 
    # Use %e format to get the n most significant digits, as a string.
    format = "%." + str(n-1) + "e"
    r = format % x
    return float(r)


def list_countries(request):
    # If this isn't an ajax request
    # if request.is_ajax() == False:
    #     # 404
    #     raise Http404

    # Otherwise
    # Filter to a list of unique countries from our life tables
    query = LifeTableEntry.objects.filter(
            is_male = True, # Assume there's a female version for each country
            age = 0, # Assume only 1 entry of age 0 for all countries
    )
    # Serialize results into a json object
    json = serializers.serialize('json', query, fields=('country'))
    # Return a json response containing a list of all potential countries
    return HttpResponse(json, mimetype='application/json')


#def life_calculation(request, country_code, year, month, day):
#    context_dict = {}
#    # If we don't have the country in the database, cache all the results
#    if LifeExpectancy.objects.filter(country_code = country_code).exists() == False:
#        if load_country(country_code) == False:
#            return HttpResponse("No Country.")
#
#    life_expectancy_query = LifeExpectancy.objects.filter(
#            country_code=country_code,
#            year_born = int(year)
#    )
#
#    # If the result doesn't exist in our current country database
#    if life_expectancy_query.exists() == False:
#        # Try fetching the new result if our database is out of date
#        if load_new_expectancy(country_code, year) == False :
#            # Otherwise use the oldest or most up to date year
#            # based on the year given
#            life_expectancies = LifeExpectancy.objects.filter(country_code=country_code).order_by('year_born') #Ascending by default
#            
#            oldest_year = life_expectancies[0]
#            # if the given birth year predates the oldest birth year use that
#            # result
#            if(int(year) <= oldest_year.year_born):
#                life_expectancy = oldest_year
#            else: #Otherwise use the newest year
#                life_expectancy = life_expectancies.reverse()[0]
#    else:
#        life_expectancy = life_expectancy_query[0]
#
#    years_expected = life_expectancy.years_expected
#    days_expected = round(years_expected * 365.242199)
#
#    birthday = date(int(year), int(month), int(day))
#    die_date = birthday + timedelta(days=days_expected)
#    remaining_time = die_date - date.today()
#    remaining_days = remaining_time.days;
#    percentage_left = remaining_days/days_expected
#
#    #return HttpResponse("Die Day: %d, %d, %d\r\nRemaining Days: %d\r\nLife Left: %.1f" 
#    #    % (die_date.year, die_date.month, die_date.day, 
#    #        remaining_days,
#    #        percentage_left * 100
#    #    )
#    #)
#
#    return render_to_response('results.html',
#                              context_dict,
#                              context_instance=RequestContext(request))
#
#       
#def load_new_expectancy(country_code, year):
#    try:
#        data = json.load(
#            urllib2.urlopen(
#                'http://api.worldbank.org/countries/'+
#                country_code + 
#                '/indicators/SP.DYN.LE00.IN?format=json&date=' +
#                str(year)
#            )
#        )
#    except ValueError:
#        return False # Can't find it in online
#
#    results = data[1]
#    if results:
#        result = results[0]
#    else:
#        return False
#
#    life_expectancy_in_years = result['value']
#    birth_year = result['date']
#
#    if life_expectancy_in_years:
#        life_expectancy = LifeExpectancy (
#                country_code=country_code,
#                year_born=birth_year,
#                years_expected=life_expectancy_in_years
#        )
#        life_expectancy.save()
#    else :
#        return False # Empty value
#
#    return True
#
#
#def load_country(country_code):
#    try:
#        data = json.load(
#            urllib2.urlopen(
#                'http://api.worldbank.org/countries/'+
#                country_code + 
#                '/indicators/SP.DYN.LE00.IN?format=json'
#            )
#        )
#    except ValueError:
#        return False
#
#    # Go through all the pages returned
#    current_page = 1; # We start on the first page
#    total_pages = data[0]['pages']
#
#    # While we haven't gone through all the pages yet
#    while current_page <= total_pages:
#        # If we need to pull another page, do so now
#        if(current_page > 1):
#            try:
#                data = json.load(
#                    urllib2.urlopen(
#                        'http://api.worldbank.org/countries/' +
#                        country_code + 
#                        '/indicators/SP.DYN.LE00.IN?format=json&page=' +
#                        str(current_page)
#                    )
#                )
#            except ValueError:
#                return False
#
#        # Get values of all the birth years and life expectancies from this
#        # page
#        for result in data[1]:
#            life_expectancy_in_years = result['value']
#            birth_year = result['date']
#            if life_expectancy_in_years:
#                life_expectancy = LifeExpectancy (
#                        country_code=country_code,
#                        year_born=birth_year,
#                        years_expected=life_expectancy_in_years
#                )
#                life_expectancy.save()
#
#        current_page += 1;
#
#    return True
