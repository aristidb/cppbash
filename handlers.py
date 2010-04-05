from tipfy import RequestHandler, request, Response
from tipfy.ext.jinja2 import render_response
from google.appengine.ext import db
from google.appengine.api import users
import models
import datetime, os

#def quote(request, key_name):
#    key = db.Key(key_name)
#    q = db.get(key)
#    if not q:
#        raise Http404
#    return render_to_response('quote.html', { 'quote': q })
#
#def review(request):
#    u = users.get_current_user()
#    if models.Reviewer.all(keys_only = True).filter('user =', u).count(1) != 1:
#        return HttpResponseRedirect(users.create_login_url("/review"))
#    q = models.Quote.all().filter('accepted =', False).order('creation_date')
#    if q.count(1) == 0:
#        return HttpResponseRedirect("/")
#    return render_to_response('review.html', { 'quotes': q })
#
#def review_submit(request, key_name):
#    if request.method != 'POST':
#        raise Http404
#    u = users.get_current_user()
#    r = models.Reviewer.all(keys_only = True).filter('user =', u).get() 
#    if not r:
#        return HttpResponseRedirect(users.create_login_url("/review"))
#    key = db.Key(key_name)
#    q = db.get(key)
#    if request.POST.get('accept', ''):
#        q.quote = request.POST['quote']
#        q.language = request.POST['language']
#        q.programming_language = request.POST['programming_language']
#        q.accepted = True
#        q.accepted_by = r
#        q.accepted_date = datetime.datetime.now()
#        q.put()
#    else:
#        q.delete()
#    return HttpResponseRedirect("/review")
