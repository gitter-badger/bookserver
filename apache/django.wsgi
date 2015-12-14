import os
import sys
path = '/opt/django/app'
if path not in sys.path:
    sys.path.append(path)


os.environ['DJANGO_SETTINGS_MODULE'] = 'bookServer.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()