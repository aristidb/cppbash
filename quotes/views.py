from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import Http404
from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
from google.appengine.api import users
from quotes import models
import datetime
import os

def home(request):
    q = models.Quote.all().filter('accepted =', True).order('creation_date')
    return render_to_response('quotes/index.html', { 'quotes': q })

def submit_form(request):
    if request.method == 'POST':
        p = request.POST
        q = models.Quote(
            quote = p['quote'],
            language = p['language'],
            programming_language = p['programming_language'],
            accepted = False)
        if p['email']:
            q.submitter_email = db.Email(p['email'])
        q.submitter_ip = os.environ['REMOTE_ADDR']
        # todo: validate
        q.put()
        return render_to_response('quotes/quote.html', { 'quote': q })
    else:
        return render_to_response('quotes/submit.html', { })

def quote(request, key_name):
    key = db.Key(key_name)
    q = db.get(key)
    if not q:
        raise Http404
    return render_to_response('quotes/quote.html', { 'quote': q })

def review(request):
    u = users.get_current_user()
    if models.Reviewer.all(keys_only = True).filter('user =', u).count(1) != 1:
        return HttpResponseRedirect(users.create_login_url("/review"))
    q = models.Quote.all().filter('accepted =', False).order('creation_date')
    if q.count(1) == 0:
        return HttpResponseRedirect("/")
    return render_to_response('quotes/review.html', { 'quotes': q })

def review_submit(request, key_name):
    if request.method != 'POST':
        raise Http404
    u = users.get_current_user()
    r = models.Reviewer.all(keys_only = True).filter('user =', u).get() 
    if not r:
        return HttpResponseRedirect(users.create_login_url("/review"))
    key = db.Key(key_name)
    q = db.get(key)
    if request.POST.get('accept', ''):
        q.quote = request.POST['quote']
        q.accepted = True
        q.accepted_by = r
        q.accepted_date = datetime.datetime.now()
        q.put()
    else:
        q.delete()
    return HttpResponseRedirect("/review")
