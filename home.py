from tipfy import RequestHandler, request, Response
from tipfy.ext.jinja2 import render_template
from google.appengine.ext import db
from google.appengine.api import users
import models

def _filter(name, request, response):
    data = request.args.get(name, None)
    if data != None:
        response.set_cookie(name, data)
        return data
    else:
        return request.cookies.get(name, None)

def _alternatives(removed, standard):
    possible = standard[:]
    possible.append('')
    if removed != None:
        possible.remove(removed)
    return possible

class HomeHandler(RequestHandler):
    def get(self, **kwargs):
        response = Response(mimetype = 'text/html')
        language = _filter('language', request, response)
        programming_language = _filter('programming_language', request, response)
        
        q = models.Quote.all()
        q.filter('accepted =', True)
        if language:
            q.filter('language =', language)
        if programming_language:
            q.filter('programming_language =', programming_language)
        q.order('-creation_date')
        
        languages = _alternatives(language, models.languages)
        programming_languages = _alternatives(programming_language, models.programming_languages)

        out = render_template(
            'index.html',
            quotes = q,
            language = language,
            languages = languages,
            programming_language = programming_language,
            programming_languages = programming_languages)

        response.response = [out]

        return response
