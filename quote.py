from tipfy import RequestHandler
from tipfy.ext.jinja2 import render_response
from tipfy.ext.db import get_or_404
from google.appengine.ext import db
import models

class QuoteViewHandler(RequestHandler):
    def get(self, **kwargs):
        key = db.Key(kwargs['key_name'])
        q = get_or_404(models.Quote, key)
        return render_response('cppbash/quote.html', quote = q)
