from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lifeleft.views.home', name='home'),
    #url(r'^lifeleft/', include('lifeleft.foo.urls')),
    url(r'^$', 'timeleft.views.main'),
    url(r'^(?P<country>.*)/(?P<gender>[MmFf])/(?P<birth_year>\d+)/(?P<birth_month>\d+)/(?P<birth_day>\d+)/',
        'timeleft.views.show_results'),
    url(r'^countries/$', 'timeleft.views.list_countries'),
    url(r'^faq/$', 'timeleft.views.faq'),
    #url(r'^(?P<country_code>\w+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/',
    #    'timeleft.views.life_calculation'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
