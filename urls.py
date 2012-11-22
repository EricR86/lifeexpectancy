from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lifeleft.views.home', name='home'),
    #url(r'^lifeleft/', include('lifeleft.foo.urls')),
    url(r'^$', direct_to_template, {'template': 'main.html'}),
    url(r'^(?P<country_code>\w+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/',
        'timeleft.views.life_calculation'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)