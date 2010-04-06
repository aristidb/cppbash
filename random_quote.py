from tipfy import RequestHandler, request, Response
from tipfy.ext.jinja2 import render_template
from google.appengine.ext import db
from werkzeug.exceptions import NotFound
import models, filters, quotejson
import random

class RandomQuoteHandler(RequestHandler):
    def get(self, **kwargs):
        json = request.is_xhr or request.args.get('json', '')

        if json:
            response = Response(mimetype = 'application/json')
        else:
            response = Response(mimetype = 'text/html')

        language = filters.filter('language', request, response)
        programming_language = filters.filter('programming_language', request, response)
        
        languages = filters.alternatives(language, models.languages)
        programming_languages = filters.alternatives(programming_language, models.programming_languages)
        
        query = models.Quote.all()
        query.filter('accepted =', True)
        if language:
            query.filter('language =', language)
        if programming_language:
            query.filter('programming_language =', programming_language)
        query.filter('random >', random.random())
        query.order('random')
        q = query.get()

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
                languages = languages,
                programming_language = programming_language,
                programming_languages = programming_languages)

        response.response = [out]

        return response
