#File to store all of the datastore models
from google.appengine.ext import ndb

class UserCredentials(ndb.Model):
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
