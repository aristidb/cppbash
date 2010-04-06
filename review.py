from tipfy import RequestHandler, request, Response, redirect, redirect_to, url_for
from tipfy.ext.jinja2 import render_response
from tipfy.ext.db import get_or_404
from google.appengine.ext import db
from google.appengine.api import users
import models
import datetime, os

class ReviewStartHandler(RequestHandler):
    def get(self, **kwargs):
        u = users.get_current_user()
        if models.Reviewer.all(keys_only = True).filter('user =', u).count(1) != 1:
            if users.is_current_user_admin():
                r = models.Reviewer(user = u)
                r.put()
            else:
                return redirect(users.create_login_url(url_for('review-start')))
        q = models.Quote.all().filter('accepted =', False).order('creation_date')
        if q.count(1) == 0:
            return redirect_to('home')
        return render_response('review.html', quotes = q)

class ReviewQuoteHandler(RequestHandler):
    def post(self, **kwargs):
        u = users.get_current_user()
        r = models.Reviewer.all(keys_only = True).filter('user =', u).get() 
        if not r:
            return redirect_to('review-start')
        key = db.Key(kwargs['key_name'])
        q = get_or_404(models.Quote, key)
        if request.form.get('accept', ''):
            q.quote = request.form['quote']
            q.language = request.form['language']
            q.programming_language = request.form['programming_language']
            q.accepted = True
            q.accepted_by = r
            q.accepted_date = datetime.datetime.now()
            q.put()
        else:
            q.delete()
        return redirect_to('review-start')
