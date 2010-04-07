from tipfy import RequestHandler, request, Response
from tipfy.ext.jinja2 import render_template
from google.appengine.ext import db
from werkzeug.exceptions import NotFound
import models, quotejson
from filters import language_filter, programming_language_filter
import random

_n = 5

class RandomQuoteHandler(RequestHandler):
    def get(self, **kwargs):
        json = request.is_xhr or request.args.get('json', '')

        if json:
            response = Response(mimetype = 'application/json')
        else:
            response = Response(mimetype = 'text/html')

        language = language_filter.make_instance(request, response)
        programming_language = programming_language_filter.make_instance(request, response)
        
        query = models.Quote.all()
        query.filter('accepted =', True)
        language.add_to_query(query)
        programming_language.add_to_query(query)
        query.filter('random >', random.random())
        query.order('random')

        qs = [ q for q in query.fetch(_n) ]

        if len(qs) < _n: # wraparound!
            query = models.Quote.all()
            query.filter('accepted =', True)
            language.add_to_query(query)
            programming_language.add_to_query(query)
            query.order('random')
            qs.extend(query.fetch(_n - len(qs)))

        if len(qs) > 0:
            q = random.choice(qs)
        else:
            q = None

        if json:
            if q == None:
                out = '[]'
            else:
                out = quotejson.json([q])
        else:
            out = render_template(
                'cppbash/random_quote.html',
                quote = q,
                language = language,
                programming_language = programming_language)

        response.response = [out]

        return response
