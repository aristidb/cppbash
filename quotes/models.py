from appengine_django.models import BaseModel
from google.appengine.ext import db

class Reviewer(BaseModel):
    user=db.UserProperty()

class Quote(BaseModel):
    creation_date=db.DateTimeProperty(auto_now = True)
    language=db.CategoryProperty()
    programming_language=db.CategoryProperty()
    quote=db.TextProperty()
    accepted=db.BooleanProperty()
    accepted_by=db.ReferenceProperty(Reviewer)
    accepted_date=db.DateTimeProperty()
    submitter_ip=db.StringProperty()
    submitter_email=db.EmailProperty()
