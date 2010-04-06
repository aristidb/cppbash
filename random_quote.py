from tipfy import RequestHandler
from tipfy.ext.jinja2 import render_response
from google.appengine.ext import db
from werkzeug.exceptions import NotFound
import models
import random

class RandomQuoteHandler(RequestHandler):
    def get(self, **kwargs):
        r = random.random()
        import sys
        sys.stderr.write(str(r) + '\n')
        query = models.Quote.all()
        query.filter('accepted =', True)
        query.filter('random >', random.random())
        query.order('random')
        q = query.get()
        if q == None:
            raise NotFound
        return render_response('quote.html', quote = q)
