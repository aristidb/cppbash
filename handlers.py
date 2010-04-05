from tipfy import RequestHandler, request, Response
from tipfy.ext.jinja2 import render_response
from google.appengine.ext import db
from google.appengine.api import users
import models
import datetime, os

#def quote(request, key_name):
#    key = db.Key(key_name)
#    q = db.get(key)
#    if not q:
#        raise Http404
#    return render_to_response('quote.html', { 'quote': q })
#
