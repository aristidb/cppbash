from tipfy import RequestHandler, request, Response
from tipfy.ext.jinja2 import render_template
from google.appengine.ext import db
from google.appengine.api import users
import models, quotejson
import filters

class HomeHandler(RequestHandler):
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

        q = models.Quote.all()
        q.filter('accepted =', True)
        if language:
            q.filter('language =', language)
        if programming_language:
            q.filter('programming_language =', programming_language)
        q.order('-creation_date')

        if json:
            out = quotejson.json(q)
        else:
            out = render_template(
                'cppbash/home.html',
                quotes = q,
                language = language,
                languages = languages,
                programming_language = programming_language,
                programming_languages = programming_languages,
                )

        response.response = [out]

        return response
