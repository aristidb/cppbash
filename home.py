from tipfy import RequestHandler, request, Response
from tipfy.ext.jinja2 import render_template
from google.appengine.ext import db
from google.appengine.api import users
import models, quotejson
from filters import language_filter, programming_language_filter

class HomeHandler(RequestHandler):
    def get(self, **kwargs):
        json = request.is_xhr or request.args.get('json', '')

        if json:
            response = Response(mimetype = 'application/json')
        else:
            response = Response(mimetype = 'text/html')

        language = language_filter.make_instance(request, response)
        programming_language = programming_language_filter.make_instance(request, response)
        
        q = models.Quote.all()
        q.filter('accepted =', True)
        language.add_to_query(q)
        programming_language.add_to_query(q)
        q.order('-creation_date')

        if json:
            out = quotejson.json(q)
        else:
            out = render_template(
                'cppbash/home.html',
                quotes = q,
                language = language,
                programming_language = programming_language)

        response.response = [out]

        return response
