from tipfy import RequestHandler, request, Response
from tipfy.ext.jinja2 import render_response
from google.appengine.ext import db
from google.appengine.api import users
import models
import datetime, os, random

class SubmitHandler(RequestHandler):
    def post(self, **kwargs):
        p = request.form
        q = models.Quote(
            quote = p['quote'],
            language = p['language'],
            programming_language = p['programming_language'],
            accepted = False)
        if p['email']:
            q.submitter_email = db.Email(p['email'])
        q.submitter_ip = os.environ['REMOTE_ADDR']
        q.creation_date = datetime.datetime.now()
        q.random = random.random()
        # todo: validate
        q.put()
        return render_response('cppbash/submit_quote.html', quote = q )

    def get(self, **kwargs):
        return render_response('cppbash/submit.html', 
                               languages = models.languages,
                               programming_languages = models.programming_languages)
