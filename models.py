from google.appengine.ext import db

languages = ['English', 'German']
default_language = 'English'
programming_languages = ['C++', 'Python', 'Haskell', 'Prolog', 'Visual Basic / Java', 'PHP']

class Reviewer(db.Model):
    user=db.UserProperty()

class Quote(db.Model):
    creation_date=db.DateTimeProperty()
    language=db.CategoryProperty()
    programming_language=db.CategoryProperty()
    quote=db.TextProperty()
    accepted=db.BooleanProperty(required = True)
    accepted_by=db.ReferenceProperty(Reviewer)
    accepted_date=db.DateTimeProperty()
    submitter_ip=db.StringProperty()
    submitter_email=db.EmailProperty()
    random=db.FloatProperty()

def accepted_quotes():
    return Quote.all().filter('accepted =', True)
