from tipfy import RequestHandler, request, Response, redirect, redirect_to, url_for
from tipfy.ext.jinja2 import render_response
from tipfy.ext.db import get_by_id_or_404
from google.appengine.ext import db
from google.appengine.api import users, mail
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
        return render_response('cppbash/review.html', quotes = q)

class ReviewQuoteHandler(RequestHandler):
    def post(self, **kwargs):
        u = users.get_current_user()
        r = models.Reviewer.all(keys_only = True).filter('user =', u).get() 
        if not r:
            return redirect_to('review-start')
        q = get_by_id_or_404(models.Quote, kwargs['id'])
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

class ReviewRemindHandler(RequestHandler):
    def get(self, **kwargs):
        q = models.Quote.all().filter('accepted =', False)
        if q.count(1) == 0:
            return Response('no reminder needed')
        rs = models.Reviewer.all()
        for r in rs:
            mail.send_mail(sender="C++ Bash <noreply@cppbash.com>",
                           to=[r.user.email() for r in rs],
                           subject="There are quotes to be reviewed",
                           body="""
Dear Reviewer,

There are new quotes to be reviewed. Please go to <http://www.cppbash.com/review>

Thank you,

the C++ Bash system
""")
        return Response('reminders sent')
