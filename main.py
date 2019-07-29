import webapp2
import os
import jinja2
from google.appengine.ext import ndb

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class UserCredentials(ndb.Model):
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)

class LoginPage(webapp2.RequestHandler):
    def get(self):
        f = open("templates/login.html", "r")
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
                self.response.write(users[0].key.integer_id())
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
            newUser = UserCredentials(username=username, password=password);
            key = newUser.put();
            self.response.write(key.integer_id());

class DashboardPage(webapp2.RequestHandler):
    def post(self):
        dashboardTemplate = jinja_env.get_template('templates/dashboard.html');
        self.response.headers['Content-Type'] = "text/html";
        values = {
            "userID": self.request.get("userID"),
            "username": UserCredentials.get_by_id(int(self.request.get("userID"))).username
        }
        self.response.write(dashboardTemplate.render(values));

app = webapp2.WSGIApplication([
    ('/', LoginPage),
    ('/login', LoginParser),
    ('/signup', SignupParser),
    ('/dashboard.html', DashboardPage)
], debug=True);
