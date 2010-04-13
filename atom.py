from tipfy import RequestHandler, request, Response, url_for
from tipfy.ext.jinja2 import render_template
from google.appengine.ext import db
import models
from filters import FilterCollection, filters

class AtomViewHandler(RequestHandler):
    def get(self, **kwargs):
        response = Response(mimetype = 'application/atom+xml')

        collection = FilterCollection(filters, request, response, cookies=False)
        
        q = models.accepted_quotes()
        collection.add_to_query(q)
        q.order('-creation_date')

        out = render_template(
            'cppbash/atom.xml',
            title = "C++ Bash",
            link = url_for('home', full=True),
            quotes = q)

        response.response = [out]

        return response
