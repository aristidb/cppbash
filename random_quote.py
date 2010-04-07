from tipfy import RequestHandler, request, Response
from tipfy.ext.jinja2 import render_template
from google.appengine.ext import db
from werkzeug.exceptions import NotFound
import models, quotejson
from filters import FilterCollection, filters
import random

_n = 5

class RandomQuoteHandler(RequestHandler):
    def get(self, **kwargs):
        json = request.is_xhr or request.args.get('json', '')

        if json:
            response = Response(mimetype = 'application/json')
        else:
            response = Response(mimetype = 'text/html')

        collection = FilterCollection(filters, request, response)
        
        query = models.accepted_quotes()
        collection.add_to_query(query)
        query.filter('random >', random.random())
        query.order('random')

        qs = [ q for q in query.fetch(_n) ]

        if len(qs) < _n: # wraparound!
            query = models.accepted_quotes()
            collection.add_to_query(query)
            query.order('random')
            qs.extend(query.fetch(_n - len(qs)))

        if len(qs) > 0:
            q = random.choice(qs)
        else:
            q = None

        if json:
            out = quotejson.single(q)
        else:
            out = render_template(
                'cppbash/random_quote.html',
                quote = q,
                filter_collection = collection)

        response.response = [out]

        return response
