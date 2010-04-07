from tipfy import RequestHandler, request, Response
from tipfy.ext.jinja2 import render_template
from google.appengine.ext import db
from google.appengine.api import users
import models, quotejson
from filters import FilterCollection, filters

class HomeHandler(RequestHandler):
    def get(self, **kwargs):
        json = request.is_xhr or request.args.get('json', '')

        if json:
            response = Response(mimetype = 'application/json')
        else:
            response = Response(mimetype = 'text/html')

        collection = FilterCollection(filters, request, response)
        
        q = models.accepted_quotes()
        collection.add_to_query(q)
        q.order('-creation_date')

        if json:
            out = quotejson.json(q)
        else:
            out = render_template(
                'cppbash/home.html',
                quotes = q,
                filter_collection = collection)

        response.response = [out]

        return response
