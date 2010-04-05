from tipfy import RequestHandler, request, Response
from tipfy.ext.jinja2 import render_template, render_response
from google.appengine.ext import db
from google.appengine.api import users
import models
import datetime, os

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
        # todo: validate
        q.put()
        return render_response('quote.html', quote = q )

    def get(self, **kwargs):
        return render_response('submit.html', 
                               languages = models.languages,
                               programming_languages = models.programming_languages)

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
