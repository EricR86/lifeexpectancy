import os
import sys

sys.path.append('/usr/local/django')
sys.path.append('/usr/local/django/lifeleft')
os.environ['DJANGO_SETTINGS_MODULE'] = 'lifeleft.production_settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
