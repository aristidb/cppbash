from appengine_django.models import BaseModel
from google.appengine.ext import db

class Quote(BaseModel):
    creation_date=db.DateTimeProperty()
    language=db.CategoryProperty()
    quote=db.TextProperty()
    accepted=db.BooleanProperty()
    submitter_ip=db.StringProperty()
    submitter_email=db.EmailProperty()

