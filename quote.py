from tipfy import RequestHandler
from tipfy.ext.jinja2 import render_response
from tipfy.ext.db import get_by_id_or_404
from google.appengine.ext import db
import models

class QuoteViewHandler(RequestHandler):
    def get(self, **kwargs):
        q = get_by_id_or_404(models.Quote, kwargs['id'])
        return render_response('cppbash/quote.html', quote = q)
