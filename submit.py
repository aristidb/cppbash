from tipfy import RequestHandler, request, Response
from tipfy.ext.jinja2 import render_response
from google.appengine.ext import db
from google.appengine.api import users
import models
import datetime, os, random

class SubmitHandler(RequestHandler):
    def post(self, **kwargs):
        p = request.form
        first = (models.Quote.all().count(1) < 1)
        q = models.Quote(
            quote = p['quote'],
            language = p['language'],
            programming_language = p['programming_language'],
            accepted = False)
        if p['email']:
            q.submitter_email = db.Email(p['email'])
        q.submitter_ip = os.environ['REMOTE_ADDR']
        q.creation_date = datetime.datetime.now()
        if not first:
            q.random = random.random()
        else:
            q.random = 1.0
        # todo: validate
        q.put()
        return render_response('quote.html', quote = q )

    def get(self, **kwargs):
        return render_response('submit.html', 
                               languages = models.languages,
                               programming_languages = models.programming_languages)
