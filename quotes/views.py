from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import Http404
from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
from quotes import models
import datetime
import os

def home(request):
    q = models.Quote.all().filter('accepted =', True).order('creation_date')
    return render_to_response('quotes/index.html', { 'quotes': q })

def submit_form(request):
    if request.method == 'POST':
        p = request.POST
        quote = models.Quote(
            quote = p['quote'],
            language = p['language'],
            programming_language = p['programming_language'],
            submitter_email = p['email'])
        # todo: validate
        quote.put()
        return HttpResponseRedirect('/')
    else:
        return render_to_response('quotes/submit.html', { })

def quote(request, key_name):
    key = db.Key(key_name)
    q = db.get(key)
    if not q:
        raise Http404
    return render_to_response('quotes/quote.html', { 'quote': q })
