from django.conf import settings
from models import Widget

try:
    widgets = settings.WIDGETS
    for group_name, params in widgets.iteritems():
        package = __import__(params['package'], fromlist=True)
        for name, verbose_name in params['items']:
            Widget.subclasses[name] = package.__dict__[name]
except:
    pass