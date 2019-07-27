import webapp2
import os
from google.appengine.ext import ndb

class UserCredentials(ndb.Model):
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)

class LoginPage(webapp2.RequestHandler):
    def get(self):
        f = open("login.html", "r")
        self.response.headers['Content-Type'] = "text/html";
        self.response.write(f.read())

class LoginParser(webapp2.RequestHandler):
    def post(self):
        username = self.request.get("username");
        password = self.request.get("password");

        self.response.headers['Content-Type'] = "text/plain";

        users = UserCredentials.query().filter(UserCredentials.username == username).fetch();

        if len(users) > 0:
            if users[0].password == password :
                self.response.write("Logged in")
            else :
                self.response.write("Incorrect password")
        else:
            self.response.write("Whoops, that username isn't in our database");

class SignupParser(webapp2.RequestHandler):
    def post(self):
        username = self.request.get("username");
        password = self.request.get("password");

        userAlreadyExists = len(UserCredentials.query().filter(UserCredentials.username == username).fetch()) > 0;
        self.response.headers['Content-Type'] = "text/plain";

        if userAlreadyExists:
            self.response.write("Sorry, that user already exists");
        else:
            self.response.write("Signed Up");
            newUser = UserCredentials(username=username, password=password);
            newUser.put();

app = webapp2.WSGIApplication([
    ('/', LoginPage),
    ('/login', LoginParser),
    ('/signup', SignupParser)
], debug=True);
