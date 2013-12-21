import os, sys
sys.path.append('/usr/local/lib/python2.7/dist-packages/django/')
sys.path.append('/home/alex/workspace/FridayEveryDay/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'FridayEveryDay.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
