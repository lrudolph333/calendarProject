import webapp2
import os

class LoginPage(webapp2.RequestHandler):
    def get(self):
        f = open("login.html", "r")
        self.response.headers['Content-Type'] = "text/html";
        self.response.write(f.read())

class LoginParser(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = "text/plain";
        self.response.write("Logged In");

class SignupParser(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = "text/plain";
        self.response.write("Signed Up");

app = webapp2.WSGIApplication([
    ('/', LoginPage),
    ('/login', LoginParser),
    ('/signup', SignupParser)
], debug=True);
