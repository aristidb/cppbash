from django.shortcuts import render_to_response
from google.appengine.ext import db
from quotes import models

def home(request):
    q = models.Quote.all().order('creation_date')
    return render_to_response('quotes/index.html', { 'quotes': q })
