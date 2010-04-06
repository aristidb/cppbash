from tipfy.ext.db import get_property_dict
from django.utils import simplejson

def json(qs):
    r = []
    for q in qs:
        d = get_property_dict(q)
        r.append({
                'creation_date': str(d['creation_date']),
                'language': str(d['language']),
                'programming_language': str(d['programming_language']),
                'quote': unicode(d['quote']),
                })
    return simplejson.dumps(r)
