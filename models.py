#File to store all of the datastore models
from google.appengine.ext import ndb

class UserCredentials(ndb.Model):
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    realName = ndb.StringProperty()

class CalendarItem(ndb.Model):
    time = ndb.StringProperty(required=True)
    date = ndb.StringProperty(required=True)
    title = ndb.StringProperty(required=True)
    location = ndb.StringProperty(required=True)
    ownerID = ndb.StringProperty(required=True)

class ToDoItem(ndb.Model):
    time = ndb.StringProperty(required=True)
    date = ndb.StringProperty(required=True)
    title = ndb.StringProperty(required=True)
    urgency = ndb.IntegerProperty(required=True)
    note = ndb.StringProperty()
