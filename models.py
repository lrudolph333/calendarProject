#File to store all of the datastore models


class UserCredentials(ndb.Model):
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)