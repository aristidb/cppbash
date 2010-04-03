from google.appengine.ext import db

class Quote(db.Model):
    creation_date=db.DateProperty()
    language=db.StringProperty()
    quote=db.StringProperty()
