from appengine_django.models import BaseModel
from google.appengine.ext import db

class Quote(BaseModel):
    creation_date=db.DateProperty()
    language=db.StringProperty()
    quote=db.StringProperty()

