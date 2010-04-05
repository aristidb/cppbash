from appengine_django.models import BaseModel
from google.appengine.ext import db

languages = ['English', 'German']
programming_languages = ['C++', 'Python', 'Haskell', 'Prolog', 'Visual Basic / Java']

class Reviewer(BaseModel):
    user=db.UserProperty()

class Quote(BaseModel):
    creation_date=db.DateTimeProperty()
    language=db.CategoryProperty()
    programming_language=db.CategoryProperty()
    quote=db.TextProperty()
    accepted=db.BooleanProperty(required = True)
    accepted_by=db.ReferenceProperty(Reviewer)
    accepted_date=db.DateTimeProperty()
    submitter_ip=db.StringProperty()
    submitter_email=db.EmailProperty()
