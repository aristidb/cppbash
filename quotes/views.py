from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
from quotes import models
import datetime
import os

def home(request):
    q = models.Quote.all().filter('accepted =', True).order('creation_date')
    return render_to_response('quotes/index.html', { 'quotes': q })

class SubmitForm(djangoforms.ModelForm):
    class Meta:
        model = models.Quote
        fields = ['language', 'quote', 'submitter_email']

def submit_form(request):
    if request.method == 'POST':
        form = SubmitForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.accepted = False
            quote.submitter_ip = os.environ['REMOTE_ADDR']
            quote.put()
            return HttpResponseRedirect('/')
    else:
        form = SubmitForm()
        return render_to_response('quotes/submit.html', {  'form': form })
